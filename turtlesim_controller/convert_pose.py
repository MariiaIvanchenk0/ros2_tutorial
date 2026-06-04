import rclpy
import math
import argparse
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, Point, Quaternion
from turtlesim.msg import Pose


class ConvertPose(Node):
    def __init__(self, output):
        super().__init__('turtlesim_convert_pose')

        self.turtle_pose = None

        # Publisher(s)
        self.pub = self.create_publisher(PoseStamped, f"/{output}/geometry_pose", 10)

        # Subscriber(s)
        self.create_subscription(Pose, "pose", self.subscriber_callback, 10)


    def subscriber_callback(self, msg):
        result_msg = PoseStamped()

        x, y, z, w = euler_to_quaternion(0.0, 0.0, msg.theta)

        result_msg.header.frame_id = "global"
        result_msg.header.stamp = self.get_clock().now().to_msg()

        result_msg.pose.position.x = msg.x  
        result_msg.pose.position.y = msg.y
        result_msg.pose.position.z = 0.0

        result_msg.pose.orientation.x = x
        result_msg.pose.orientation.y = y
        result_msg.pose.orientation.z = z 
        result_msg.pose.orientation.w = w
        
        self.pub.publish(result_msg)


def euler_to_quaternion(roll, pitch, yaw):
    """
    Convert Euler angles (roll, pitch, yaw) to quaternion.

    Args:
        roll  : Rotation around X-axis (radians)
        pitch : Rotation around Y-axis (radians)
        yaw   : Rotation around Z-axis (radians)

    Returns:
        (qx, qy, qz, qw) : tuple of 4 floats
    """

    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)

    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)

    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return qx, qy, qz, qw



def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True)
    args, unknown_args = parser.parse_known_args()

    rclpy.init(args=unknown_args)

    node = ConvertPose(output=args.output)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
