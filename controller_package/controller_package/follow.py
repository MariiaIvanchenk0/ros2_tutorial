import math
import rclpy
import argparse
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point

class FollowNode(Node):
    def __init__(self, output):
        super().__init__('follow')

        self.goal = None
        self.safe_distance = 0.3
        self.Kp_linear = 0.6
        self.Kp_angular = 1.5
        
        self.pub = self.create_publisher(Twist, f"/{output}/cmd_vel", 10) # robot_1

        self.create_subscription(Point, '/aruco_position', self.position_callback, 10)

        self.create_timer(0.1, self.timer_callback)

    def position_callback(self, msg):
        self.goal = [msg.x, msg.y, msg.z]

    def timer_callback(self):
        msg = Twist()

        if self.goal is not None:

            distance_error = self.goal[2] - self.safe_distance
            if abs(distance_error) > 0.05:
                msg.linear.x = self.Kp_linear * distance_error
            else:
                msg.linear.x = 0.0

            heading_error = math.atan2(self.goal[0], self.goal[2])
            msg.angular.z = self.Kp_angular * heading_error
                    
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

    try:
      rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop_robot()


    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()