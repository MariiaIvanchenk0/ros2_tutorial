import math
import rclpy
from rclpy.node import Node
import argparse
from geometry_msgs.msg import PoseStamped, Twist
from vicon_test_control.control_law import compute_go_to_goal_control


class GoToGoalNode(Node):
    def __init__(self, output):
        super().__init__('go_to_goal')

        self.pose = None
        self.goal = None

        # attributed of classes (local variables)
        
        # Controller parameters
        
        # Publisher(s) 
        self.pub = self.create_publisher(Twist, f"/{output}/cmd_vel", 10)

        # Subscriber(s)
        self.create_subscription(PoseStamped, "robot_pose", self.subscriber_callback, 10)

        self.create_subscription(PoseStamped, "goal", self.goal_callback, 10)

        # Timer (for loops if any)
        self.create_timer(0.1, self.timer_callback)

    def goal_callback(self, msg:PoseStamped):
       self.goal = [msg.pose.position.x, msg.pose.position.y]
    

    def subscriber_callback(self, received_msg: PoseStamped):
        q = received_msg.pose.orientation

        yaw = quaternion_to_yaw(
            q.x,
            q.y,
            q.z,
            q.w
        )

        self.pose = [
            received_msg.pose.position.x,
            received_msg.pose.position.y,
            yaw
        ]

    def timer_callback(self):
        msg = Twist()

        if self.pose is not None:
            v, w = compute_go_to_goal_control(self.pose, self.goal)
            msg.linear.x = v # 1.0
            msg.angular.z = w # 0.5
            
        self.pub.publish(msg)
        self.get_logger().info(f'pose(x): {self.pose[0]}, pose(y): {self.pose[1]}, pose(yaw): {self.pose[2] * 180.0 / math.pi}.\n')
        # self.get_logger().info(f'goal(x): {self.goal[0]}, goal(y): {self.goal[1]}.\n')


def quaternion_to_yaw(x, y, z, w):
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str)
    args, unknown_args = parser.parse_known_args()

    rclpy.init(args=unknown_args)

    node = GoToGoalNode(output=args.output)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()