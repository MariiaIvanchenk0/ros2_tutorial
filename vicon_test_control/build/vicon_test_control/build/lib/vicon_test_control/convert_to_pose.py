#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from vicon_receiver.msg import Position


class PoseConverter(Node):

    def __init__(self):
        super().__init__('convert_to_pose')

        self.subscription = self.create_subscription(
            Position,
            '/vicon/agent1/agent1',
            self.pose_callback,
            10
        )

        self.publisher = self.create_publisher(
            PoseStamped,
            '/robot_pose',
            10
        )

    def pose_callback(self, msg):
        pose_msg = PoseStamped()

        # Header
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "map"

        # Position
        pose_msg.pose.position.x = - float(msg.y_trans) / 1000.0
        pose_msg.pose.position.y = float(msg.x_trans) / 1000.0
        pose_msg.pose.position.z = float(msg.z_trans) / 1000.0

        # Orientation (quaternion)
        pose_msg.pose.orientation.x = float(msg.x_rot)
        pose_msg.pose.orientation.y = float(msg.y_rot)
        pose_msg.pose.orientation.z = float(msg.z_rot)
        pose_msg.pose.orientation.w = float(msg.w)

        self.publisher.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)

    node = PoseConverter()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()