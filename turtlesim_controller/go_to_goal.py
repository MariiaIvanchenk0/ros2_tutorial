import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Point
from turtlesim.msg import Pose
from turtlesim_controller.control_law import compute_go_to_goal_control

class GoToGoalNode(Node):
    def __init__(self, namespace='turtle1'):
        super().__init__('turtlesim_go_to_goal')

        self.pose = None
        self.goal = None

        # attributed of classes (local variables)
        
        # Controller parameters
        
        # Publisher(s) 
        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        # Subscriber(s)
        self.create_subscription(Pose, "turtle1/pose", self.subscriber_callback, 10)

        self.create_subscription(Pose, "turtle1/goal", self.goal_callback, 10)

        # Timer (for loops if any)
        self.create_timer(0.1, self.timer_callback)

    def goal_callback(self, msg):
       self.goal = [msg.x, msg.y]
    
    def subscriber_callback(self, recieved_msg):
        self.pose = [
            recieved_msg.x, 
            recieved_msg.y,
            recieved_msg.theta]

    def timer_callback(self):
        msg = Twist()

        if self.pose is not None:
            v, w = compute_go_to_goal_control(self.pose, self.goal)
            msg.linear.x = v # 1.0
            msg.angular.z = w # 0.5
            
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    node = GoToGoalNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()