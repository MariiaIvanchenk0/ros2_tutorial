import math
import rclpy
import argparse
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist, Point
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import TransitionCallbackReturn

class FollowLifecycleNode(LifecycleNode):
    def __init__(self, output):
        super().__init__('follow')

        self.follow_enabled = False
        self.goal = None
        self.last_seen = None
        self.output = output

        self.declare_parameter('safe_distance', 0.3)
        self.declare_parameter('Kp_linear', 0.4)
        self.declare_parameter('Kp_angular', 0.3)
        # safety / smoothing
        self.declare_parameter('max_linear', 0.25)        # m/s
        self.declare_parameter('max_angular', 0.8)        # rad/s
        self.declare_parameter('distance_deadband', 0.05) # m
        self.declare_parameter('lateral_deadband', 0.03)  # m, ignore tiny offsets
        self.declare_parameter('heading_deadband', 0.05)  # rad
        self.declare_parameter('lost_timeout', 0.5)       # s, stop if no marker

    
    def on_configure(self, state):
        """
        Handles transition from Unconfigured to Inactive.
        Set up publishers, subscribers, and parameters here.
        """
        self.get_logger().info("Configuring node...")

        self.enable = self.create_service(Empty, f'/{self.output}/enable_follow', self.enable_follow_callback)
        self.disable = self.create_service(Empty, f'/{self.output}/disable_follow', self.disable_follow_callback)
        
        self.sub = self.create_subscription(Point, f'/{self.output}/aruco_position', self.position_callback, 10)
        self.pub = self.create_lifecycle_publisher(Twist, f"/{self.output}/cmd_vel", 10)
        
        return TransitionCallbackReturn.SUCCESS
    
    def on_activate(self, state):
        """
        Handles transition from Inactive to Active.
        Activate your lifecycle publishers here.
        """
        try: 
            self.get_logger().info("Activating node...")
            if self.pub is not None:
                self.pub.on_activate(state)
            
            self.timer = self.create_timer(0.1, self.timer_callback)
            return super().on_activate(state)
            # return TransitionCallbackReturn.SUCCESS

        except Exception as e:
            # This will print the exact line and message that caused the crash!
            self.get_logger().error(f"ACTIVATION CRASHED: {str(e)}", throttle_duration_sec=1.0)
            return TransitionCallbackReturn.FAILURE

    
    def on_deactivate(self, state):
        """
        Handles transition from Active to Inactive.
        Deactivate publishers and stop timers/processing.
        """
        self.get_logger().info("Deactivating node...")
        self.stop_robot()
        if self.pub is not None:
            self.pub.on_deactivate(state)
        
        return super().on_deactivate(state)
        # return TransitionCallbackReturn.SUCCESS


    def on_cleanup(self, state):
        """
        Handles transition from Inactive to Unconfigured.
        Clean up resources and destroy publishers/timers.
        """
        self.get_logger().info("Cleaning up node...")
        

        if self.enable: self.destroy_service(self.enable)
        if self.disable: self.destroy_service(self.disable)
        if self.sub: self.destroy_subscription(self.sub)
        if self.pub: self.destroy_publisher(self.pub)

        self.goal = None
        self.last_seen = None
        
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state):
        """
        Handles transition to the Finalized state from any state.
        """
        self.get_logger().info("Shutting down node...")
        try:
            self.stop_robot()
        except Exception:
            pass
        return TransitionCallbackReturn.SUCCESS

    def enable_follow_callback(self, request, response):
        self.follow_enabled = True
        self.get_logger().info("Follow is ON.")
        return response
    
    def disable_follow_callback(self, request, response):
        self.follow_enabled = False
        self.get_logger().info("Follow is OFF.")
        return response

    def position_callback(self, msg):
        # read_aruco publishes (0, 0, 0) when nothing is detected -> ignore it
        if msg.x == 0.0 and msg.y == 0.0 and msg.z == 0.0:
            return
        self.goal = [msg.x, msg.y, msg.z]
        self.last_seen = self.get_clock().now()

    def timer_callback(self):
        safe_distance = self.get_parameter('safe_distance').value
        Kp_linear = self.get_parameter('Kp_linear').value
        Kp_angular = self.get_parameter('Kp_angular').value
        max_linear = self.get_parameter('max_linear').value
        max_angular = self.get_parameter('max_angular').value
        distance_deadband = self.get_parameter('distance_deadband').value
        lateral_deadband = self.get_parameter('lateral_deadband').value
        heading_deadband = self.get_parameter('heading_deadband').value
        lost_timeout = self.get_parameter('lost_timeout').value

        if self.pub is None or not self.pub.is_activated:
            return
        
        # --- marker-loss safety: stop if disabled, no goal, or detection is stale ---
        marker_visible = (
            self.follow_enabled and
            self.goal is not None
            and self.last_seen is not None
            and (self.get_clock().now() - self.last_seen).nanoseconds * 1e-9 < lost_timeout
        )

        if not marker_visible:
            # forget the stale target and reset the filter so we don't lurch on re-acquire
            self.goal = None
            self.pub.publish(Twist())  # all zeros -> robot stops
            return

        x, _, z = self.goal  # x = lateral (right +), z = forward distance

        # --- distance control (forward/back to hold safe_distance) ---
        distance_error = z - safe_distance
        if abs(distance_error) <= distance_deadband:
            v = 0.0
        else:
            v = Kp_linear * distance_error

        # --- heading control (ignore tiny lateral offsets) ---
        if abs(x) <= lateral_deadband:
            heading_error = 0.0
        else:
            heading_error = -math.atan2(x, z)

        if abs(heading_error) <= heading_deadband:
            w = 0.0
        else:
            w = Kp_angular * heading_error

        # turn first, drive later: scale forward speed down during large turns
        v *= max(0.0, math.cos(heading_error))

        # --- saturate so a noisy spike can never command a violent move ---
        v = max(-max_linear, min(max_linear, v))
        w = max(-max_angular, min(max_angular, w))

        msg = Twist()
        msg.linear.x = v
        msg.angular.z = w
        self.pub.publish(msg)

        self.get_logger().info(f'linear.x: {msg.linear.x:.3f}, angular.z: {msg.angular.z:.3f}.\n')

    def stop_robot(self):
        if self.pub is not None and self.pub.is_activated:
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            
            for _ in range(3):
                self.pub.publish(msg)

            self.get_logger().info(f'linear.x: {msg.linear.x}, angular.z: {msg.angular.z} --> Stop.\n')


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str)
    args, unknown_args = parser.parse_known_args()

    rclpy.init(args=unknown_args)
    node = FollowLifecycleNode(output=args.output)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop_robot()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
