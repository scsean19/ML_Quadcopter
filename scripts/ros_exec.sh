#!/bin/bash

exec docker exec -it ros_jazzy_perception \
  bash -ic "source /opt/ros/jazzy/setup.bash && \
            [ -f /home/pihost/ros2_ws/install/setup.bash ] && source /home/pihost/ros2_ws/install/setup.bash; \
            exec bash"
