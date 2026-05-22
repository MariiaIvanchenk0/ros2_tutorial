from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
    
        # ros2 run turtlesim turtlesim_node
        Node(
            package='turtlesim_controller',
            # namespace='turtle1',
            executable='turtlesim_node',
        ),

        # ros2 service call /spawn turtlesim/srv/Spawn
        TimerAction(
            period=2.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'service', 'call',
                        '/spawn',
                        'turtlesim/srv/Spawn',
                    ],
                    output='screen'
                )
            ]
        )

        # # ros2 run turtlesim turtle_teleop_key /turtle1/cmd_vel:=/turtle2/cmd_vel
        # Node(
        #     package='turtlesim',
        #     executable='turtle_teleop_key',
        #     remappings=[('/turtle1/cmd_vel', '/turtle2/cmd_vel')]
        # )

        # ros2 run turtlesim_controller go_to_goal --ros-args -r /turtle1/goal:=/turtle2/pose
        Node(
            package='turtlesim_controller',
            executable='go_to_goal',
            remappings=[('/turtle1/goal', '/turtle2/pose')]
        )

        # ros2 run turtlesim_controller convert_pose_node --ros-args -r __ns:=/turtle1
        Node(
            package='turtlesim_controller',
            executable='convert_pose_node',
            namespace='turtle1'
        )

        # ros2 run turtlesim_controller convert_pose_node --ros-args -r __ns:=/turtle2
        Node(
            package='turtlesim_controller',
            executable='convert_pose_node',
            namespace='turtle2'
        )

        # rviz2
            TimerAction(
                period=2.0,
                actions=[
                    ExecuteProcess(
                        cmd=[
                            'rviz2',
                        ],
                        output='screen'
                    )
                ]
            )
    ])