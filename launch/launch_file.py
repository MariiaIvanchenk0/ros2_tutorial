from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node

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
            remappings=[('goal', '/turtle2/pose')]
        ),

        # ros2 run turtlesim_controller turtle_pose_convert_node --output robot1 --ros-args -r __ns:=/turtle1
        Node(
            package='turtlesim_controller',
            executable='turtle_pose_convert_node',
            namespace='turtle1', 
            parameters=['--output', 'robot1']
        ),

        # ros2 run turtlesim_controller turtle_pose_convert_node --output robot2 --ros-args -r __ns:=/turtle2
        Node(
            package='turtlesim_controller',
            executable='turtle_pose_convert_node',
            namespace='turtle2',
            parameters=['--output', 'robot2']
        ),

        # rviz2
        # TimerAction(
        #     period=2.0,
        #     actions=[
        # ExecuteProcess(
        #     cmd=[
        #         'rviz2',
        #     ],
        #     output='screen'
        # )
        #     ]
        # )
    ])