import math
import rclpy
import argparse
from rclpy.node import Node
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist, Point

class FollowNode(Node):
    def __init__(self, output):
        super().__init__('follow')

        self.follow_enabled = False
        self.goal = None
        self.safe_distance = 0.3
        self.Kp_linear = 0.4
        self.Kp_angular = 0.3

        self.enable = self.create_service(Empty, f'/{output}/enable_follow', self.enable_follow_callback)
        self.disable = self.create_service(Empty, f'/{output}/disable_follow', self.disable_follow_callback)
        
        self.pub = self.create_publisher(Twist, f"/{output}/cmd_vel", 10) # robot_1

        self.create_subscription(Point, f'/{output}/aruco_position', self.position_callback, 10)

        self.create_timer(0.1, self.timer_callback)
    
    def enable_follow_callback(self, request, response):
        self.follow_enabled = True
        self.get_logger().info("Follow is ON.")
        return response
    
    def disable_follow_callback(self, request, response):
        self.follow_enabled = False
        self.get_logger().info("Follow is OFF.")
        return response

    def position_callback(self, msg):
        self.goal = [msg.x, msg.y, msg.z]

    def timer_callback(self):
        msg = Twist()

        if self.follow_enabled and self.goal is not None:
            distance_error = self.goal[2] - self.safe_distance
            heading_error = -math.atan2(self.goal[0], self.goal[2])

            if abs(distance_error) <= 0.05:
                msg.linear.x = 0.0
            else:
                msg.linear.x = self.Kp_linear * distance_error

            if abs(heading_error) > 0.05:
                msg.angular.z = self.Kp_angular * heading_error
            else:
                msg.angular.z = 0.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.pub.publish(msg)

        self.get_logger().info(f'linear.x: {msg.linear.x}, angular.z: {msg.angular.z}.\n')

    def stop_robot(self):
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
    
    node = FollowNode(output=args.output)
#    executor = MultiThreadedExecutor()
#    executor.add_node(node)

    try:
        rclpy.spin(node)
#    executor.spin()
    except KeyboardInterrupt:
        node.stop_robot()


    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
