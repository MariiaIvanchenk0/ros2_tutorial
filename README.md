# ros2_tutorial
```
mkdir -p mariia_ws/src
cd src
git clone link turtlesim_controller
```

```
colcon build --packages-select turtlesim_controller 
source install/setup.bash 
ros2 launch turtlesim_controller launch_file.py
```

```
ros2 run turtlesim turtle_teleop_key /turtle1/cmd_vel:=/turtle2/cmd_vel
```
