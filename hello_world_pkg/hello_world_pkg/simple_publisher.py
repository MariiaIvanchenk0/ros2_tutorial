import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Empty

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')

        self.create_service(Empty, 'enable_control', self.enable_service_callback)
        self.enable = False

        self.create_service(Empty, 'disable_control', self.disable_service_callback)

        self.publisher_ = self.create_publisher(String, 'jetson_test_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        if self.enable:
            msg = String()
            msg.data = 'jetson Docker is communicating!'
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing: "{msg.data}"')

    def enable_service_callback(self, request:Empty.Request, response:Empty.Response):
        self.enable = True
        return response

    def disable_service_callback(self, request:Empty.Request, response:Empty.Response):
        self.enable = False
        return response

def main(args=None):
    rclpy.init(args=args)
    node = SimplePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()