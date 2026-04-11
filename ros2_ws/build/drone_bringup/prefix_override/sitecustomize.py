import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sean/projects/ML_Quadcopter/ros2_ws/install/drone_bringup'
