import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node

config_file = os.path.join(get_package_share_directory('turtlesim_controller'), 'config', 'config.yaml')
rviz_config = os.path.join(get_package_share_directory('turtlesim_controller'), 'config', 'config.rviz')

def generate_launch_description():
    return LaunchDescription([
    
        # ros2 run turtlesim turtlesim_node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
        ),

        # ros2 service call /spawn turtlesim/srv/Spawn
        # TimerAction(
        #     period=2.0,
        #     actions=[
        ExecuteProcess(
            cmd=[
                'ros2', 'service', 'call',
                '/spawn',
                'turtlesim/srv/Spawn',
            ],
            output='screen'
        ),
        #     ]
        # ),

        # ros2 run turtlesim_controller go_to_goal_node --ros-args -r /turtle1/goal:=/turtle2/pose
        Node(
            name='go_to_goal',
            package='turtlesim_controller',
            executable='go_to_goal_node',
            namespace='turtle1',
            remappings=[('goal', '/turtle2/pose')],
            parameters=[config_file],
        ),

        # ros2 run turtlesim_controller turtle_pose_convert_node --output robot1 --ros-args -r __ns:=/turtle1
        Node(
            package='turtlesim_controller',
            executable='turtle_pose_convert_node',
            namespace='turtle1', 
            arguments=['--output', 'robot1']
        ),

        # ros2 run turtlesim_controller turtle_pose_convert_node --output robot2 --ros-args -r __ns:=/turtle2
        Node(
            package='turtlesim_controller',
            executable='turtle_pose_convert_node',
            namespace='turtle2',
            arguments=['--output', 'robot2']
        ),

        # rviz2
        # TimerAction(
        #     period=2.0,
        #     actions=[
        ExecuteProcess(
            cmd=[
                'ros2', 'run', 'rviz2', 'rviz2', '-d', 'config_rviz'
            ],
            output='screen',
        )
        #     ]
        # )
    ])