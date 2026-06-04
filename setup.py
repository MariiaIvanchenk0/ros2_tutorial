import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtlesim_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (
        os.path.join('share', 'ament_index', 'resource_index', 'packages'),
        [os.path.join('resource', package_name)]
    ),
    (
        os.path.join('share', package_name),
        ['package.xml']
    ),
    (
        os.path.join('share', package_name, 'launch'),
        glob(os.path.join('launch', 'launch*.[pxy][yma]*'))
    ),
    (
        os.path.join('share', package_name, 'config'),
        glob(os.path.join('config', '*.yaml')) +
        glob(os.path.join('config', '*.rviz')))
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