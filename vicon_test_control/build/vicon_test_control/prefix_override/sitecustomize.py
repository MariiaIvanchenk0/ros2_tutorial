import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mission-control/mariia_tutorial_ws/src/turtlesim_controller/vicon_test_control/install/vicon_test_control'
