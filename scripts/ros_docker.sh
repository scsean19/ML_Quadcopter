#!/bin/bash

exec docker run -it --rm \
  --name ros_jazzy_perception \
  --network host \
  --privileged \
  -e ROS_DOMAIN_ID=7 \
  -e ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET \
  -e PYTHONPATH=/opt/perception_venv/lib/python3.12/site-packages \
  -v /dev:/dev \
  -v /run/udev:/run/udev:ro \
  -v "$HOME:/home/pihost" \
  ros_jazzy_perception \
  bash -ic "source /opt/ros/jazzy/setup.bash && \
            [ -f /home/pihost/ros2_ws/install/setup.bash ] && source /home/pihost/ros2_ws/install/setup.bash; \
            exec bash"
