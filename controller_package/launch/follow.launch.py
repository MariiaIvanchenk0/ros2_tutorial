from launch import LaunchDescription
# from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # ros2 run controller_package aruco_reader_node
        Node(
            package='controller_package',
            executable='aruco_reader_node',
        ),

        # ros2 run controller_package follow_node --output robot_1
        Node(
            package='controller_package',
            executable='follow_node',
            arguments=['--output', 'robot_1']
        )
    ])