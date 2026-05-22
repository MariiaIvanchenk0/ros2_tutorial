from setuptools import find_packages, setup

package_name = 'turtlesim_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        ('share/' + package_name + '/launch', ['launch/launch_file.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pi31415',
    maintainer_email='pi31415@example.com',
    description='Turtlesim controller package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'go_to_goal_node = turtlesim_controller.go_to_goal:main',
            'turtle_pose_convert_node = turtlesim_controller.convert_pose:main',
        ],
    },
)