FROM ros:jazzy

RUN apt update && apt install -y \
    ros-jazzy-cv-bridge \
    ros-jazzy-camera-ros \
    python3-opencv \
    libcamera-dev \
    libcamera-tools \
    v4l-utils \
    python3-pip \
    python3-venv \
    python3-numpy \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/perception_venv

RUN /opt/perception_venv/bin/pip install --upgrade pip

RUN /opt/perception_venv/bin/pip install \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch \
    torchvision \
    ultralytics \
    numpy==1.26.4 \
    opencv-python==4.10.0.84

ENV PATH="/opt/perception_venv/bin:$PATH"
ENV PYTHONPATH="/opt/perception_venv/lib/python3.12/site-packages"
ENV ROS_DOMAIN_ID=7
ENV ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET

CMD ["bash"]
