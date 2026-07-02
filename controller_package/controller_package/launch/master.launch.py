import os
from launch_ros.actions import LifecycleNode
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node, PushRosNamespace

params_file = os.path.join(get_package_share_directory('controller_package'), 'config', 'params.yaml')

def generate_launch_description():

    custom_node = Node(
	namespace='robot_1',
        package='hello_world_pkg',
        executable='simplepub',
    	output='screen'
    )

    # ros2 run controller_package aruco_reader_node
    aruco_reader = Node(
	namespace='robot_1',
        package='controller_package',
        executable='aruco_reader_node',
	    arguments=['--output', 'robot_1'],
    )

    # ros2 run controller_package follow_node --output robot_1
    follow = LifecycleNode(
	name='follow_lifecycle',
	namespace='robot_1',
        package='controller_package',
        executable='follow_node',
        arguments=['--output', 'robot_1'],
        parameters=[params_file]
    )

    return LaunchDescription([
       # PushRosNamespace('robot_1'),
        custom_node,
        aruco_reader,
        #follow
    ])
