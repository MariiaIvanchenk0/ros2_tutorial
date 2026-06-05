from setuptools import find_packages, setup

package_name = 'vicon_test_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mission-control',
    maintainer_email='mariiaivanchenko027@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'go_to_goal_node = vicon_test_control.go_to_goal:main',
            'convert_to_pose_node = vicon_test_control.convert_to_pose:main',
        ],
    },
)
