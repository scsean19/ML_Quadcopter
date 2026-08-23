# ML_Quadcopter

**Machine Learning–Enabled Autonomous Quadcopter Platform**

## Overview

This project focuses on building an **autonomous quadcopter system** capable of perception-driven flight using machine learning and robotics frameworks.

The platform integrates:

* **Pixhawk 2.4.8** flight controller running **ArduPilot**
* **ROS2 Jazzy** robotics middleware
* **Raspberry Pi 5** companion computer
* **YOLOv8-based human detection**
* **MAVLink communication via MAVROS**
* Planned hardware-accelerated inference using **Google Coral USB TPU**

The long-term objective is to develop a drone capable of **detecting and tracking humans autonomously** while maintaining safe and stable flight behavior.

---

## System Architecture

Below is the high-level architecture of the system:

![Drone Architecture](/docs/diagrams/docs_architecture.png)

Core system flow:

    Camera
      ↓
    YOLO Perception
      ↓
    ROS2 Tracking Logic
      ↓
    MAVROS
      ↓
    Pixhawk / ArduPilot
      ↓
    Flight Control

The Raspberry Pi companion computer handles perception and high-level decision-making, while the Pixhawk flight controller maintains low-level flight stability.

---

## Hardware Configuration

| Component | Model |
| --- | --- |
| Flight Controller | Pixhawk 2.4.8 |
| Firmware | ArduPilot (ArduCopter) |
| Companion Computer | Raspberry Pi 5 (8GB) |
| Camera | Raspberry Pi Camera Module |
| ML Accelerator (Planned) | Google Coral USB TPU |
| GPS | u-blox M8N |
| ESC | 4-in-1 BLHeli_32 |
| Frame | 10" quad configuration |

---

## Software Stack

| Layer | Technology |
| --- | --- |
| Flight Control | ArduPilot |
| Middleware | ROS2 Jazzy |
| Communication | MAVLink / MAVROS |
| Vision | Python + OpenCV |
| Object Detection | YOLOv8 / Ultralytics |
| Machine Learning | PyTorch |
| Edge Inference (Planned) | TensorFlow Lite / Coral Edge TPU |
| Visualization | RViz2 / rqt |
| Ground Control | QGroundControl |
| Containerization | Docker |

---

## Current Status

🚧 **Active Development**

Current progress includes:

* ROS2 Jazzy installed and operational
* MAVROS successfully communicating with Pixhawk
* IMU and telemetry data streaming through ROS2
* Docker-based ROS2 perception environment configured
* Raspberry Pi camera streaming into ROS2 at approximately 10 Hz
* YOLOv8 person detection running on the Raspberry Pi 5
* Highest-confidence person target selection
* Real-time target-center and image-center error calculation
* Annotated perception stream with bounding-box and tracking visualization
* ROS2 perception topics accessible from a remote Linux workstation
* Hardware platform assembled and operational

---

## Development Roadmap

This project follows a staged development process progressing from hardware integration to autonomous perception and control.

---

### Phase 1 — Hardware Platform Assembly ✅ (Completed)

Core flight hardware assembled and validated.

Completed:

* [x] Frame assembly and motor installation
* [x] ESC installation and wiring
* [x] Pixhawk 2.4.8 installation
* [x] GPS module installation (u-blox M8N)
* [x] Power distribution and battery integration
* [x] RC receiver installation
* [x] Initial hardware validation and bench testing
* [x] Companion computer (Raspberry Pi 5) integration
* [x] Camera mounting and positioning
* [x] System architecture design

---

### Phase 2 — Flight Controller & Communication Integration ✅ (Completed)

Flight controller configured and communication established.

Completed:

* [x] ArduPilot firmware installation
* [x] QGroundControl configuration
* [x] MAVLink communication validation
* [x] MAVROS integration with ROS2 Jazzy
* [x] Telemetry verification
* [x] IMU data streaming to ROS2 topics
* [x] ROS2 environment containerized using Docker
* [x] ROS2 workspace created and validated

---

### Phase 3 — Perception System Integration 🚧 (In Progress)

Developing and validating real-time vision-based perception and target tracking.

Completed:

* [x] Raspberry Pi camera capture pipeline
* [x] Camera-to-ROS2 TCP bridge
* [x] `/camera/image_raw` publishing at approximately 10 Hz
* [x] YOLOv8 integration with ROS2
* [x] Real-time person detection
* [x] Highest-confidence person target selection
* [x] Bounding-box center calculation
* [x] Horizontal and vertical tracking-error calculation
* [x] Annotated perception stream published to `/camera/yolo_annotated`
* [x] Bounding-box visualization
* [x] Camera-center crosshair visualization
* [x] Target-center visualization
* [x] Tracking-error vector visualization
* [x] Remote perception-stream visualization from Linux workstation

In Progress:

* [ ] Detection performance benchmarking
* [ ] Target tracking robustness testing
* [ ] Perception pipeline optimization

---

## Perception Demo

The current perception pipeline performs real-time person detection using **YOLOv8** on the Raspberry Pi 5.

Camera frames are captured using the Raspberry Pi camera stack and streamed into the ROS2 environment. The ROS2 perception node subscribes to `/camera/image_raw`, performs inference, and selects the highest-confidence detected person as the current tracking target.

For the selected target, the node calculates:

* Bounding-box coordinates
* Target center position
* Horizontal error from camera center
* Vertical error from camera center

The annotated debugging stream displays:

* YOLO person bounding box
* Detected target center
* Dashed camera-center crosshair
* Error vector between camera center and target center

Detection information is published to:

    /detections

The annotated video stream is published to:

    /camera/yolo_annotated

### Current CPU Baseline

Initial testing on the Raspberry Pi 5 CPU produced approximately:

| Pipeline Stage | Rate |
| --- | ---: |
| Camera input | ~10 Hz |
| YOLOv8 annotated output | ~3 Hz |

This provides a baseline for future inference optimization and Coral Edge TPU acceleration.

### Demo Video

[View YOLO Person Tracking Demo](demos/yolo_person_tracking.mp4)

---

### Phase 4 — Edge Inference Deployment

Deploy optimized machine learning models to embedded hardware.

Planned:

* [ ] Establish CPU inference performance baseline
* [ ] Convert or adapt detection model for TensorFlow Lite
* [ ] Compile compatible model for Coral Edge TPU
* [ ] Deploy inference to Coral USB TPU
* [ ] Benchmark CPU vs. TPU inference performance
* [ ] Optimize inference latency and resource utilization
* [ ] Validate real-time detection performance

---

### Phase 5 — Autonomous Behavior Development

Use perception output to drive autonomous tracking behavior.

Planned:

* [ ] Normalize image-space tracking error
* [ ] Develop target tracking control logic
* [ ] Integrate tracking output with MAVROS
* [ ] Implement position/attitude control interface
* [ ] Add tracking deadbands and control limits
* [ ] Implement target-loss behavior
* [ ] Validate safety constraints
* [ ] Conduct controlled flight testing

---

### Phase 6 — Advanced Autonomy & Navigation

Expand capabilities for real-world autonomy.

Future Work:

* [ ] Visual navigation
* [ ] SLAM integration
* [ ] Multi-object tracking
* [ ] Mission planning
* [ ] Sensor fusion (IMU + GPS + Vision)

---

## Current Focus

**Active Phase: Phase 3 — Perception System Integration**

The current development focus is validating and improving the real-time perception pipeline before connecting vision-based tracking information to autonomous flight behavior.

The current system can detect a person, determine the target's position relative to the center of the camera image, and publish this information through ROS2 for downstream control development.

---

## Verified System Capabilities

The following system functions have been successfully validated:

* MAVROS communication with Pixhawk
* ROS2 telemetry and IMU topic streaming
* Dockerized ROS2 environment
* Raspberry Pi camera capture
* Camera-to-ROS2 streaming at approximately 10 Hz
* YOLOv8 person detection on Raspberry Pi 5
* Highest-confidence person target selection
* Target bounding-box center calculation
* Horizontal and vertical image-center tracking error
* Annotated perception visualization
* ROS2 perception output accessible from remote workstation
* Ground control telemetry

---

## Repository Structure

    ML_Quadcopter/
    │
    ├── data/
    │
    ├── demos/
    │   └── yolo_person_tracking.mp4
    │
    ├── docker/
    │   └── ros2_camera.Dockerfile
    │
    ├── docs/
    │   ├── diagrams/
    │   └── wiring/
    │
    ├── models/
    │
    ├── ros2_ws/
    │   └── drone_bringup/
    │       ├── drone_bringup/
    │       │   ├── camera_node.py
    │       │   ├── camera_receiver_node.py
    │       │   ├── stream_bridge_node.py
    │       │   └── yolo_detector_node.py
    │       ├── package.xml
    │       ├── setup.cfg
    │       └── setup.py
    │
    ├── scripts/
    │   ├── camera_bridge_sender.py
    │   ├── ros_docker.sh
    │   └── ros_exec.sh
    │
    └── README.md

---

## Key Features

### Implemented

* ROS2-based modular architecture
* Pixhawk/ArduPilot communication through MAVROS
* Raspberry Pi camera integration
* Real-time YOLOv8 person detection
* Person target selection
* Image-space tracking-error calculation
* Annotated perception visualization
* Dockerized perception environment

### Planned

* Hardware-accelerated inference using Coral Edge TPU
* Closed-loop autonomous person tracking
* Perception-driven flight control
* Advanced navigation and sensor fusion

---

## Safety Considerations

⚠️ Always follow safe drone development practices:

* Remove propellers during bench testing
* Use a bench power supply when possible
* Verify flight-controller failsafe configuration
* Validate perception and control logic before live flight
* Apply limits to autonomous control commands
* Provide manual pilot override
* Monitor system telemetry during testing

---

## Project Goal

The goal of this project is to develop an end-to-end autonomous robotics platform combining **embedded computing, computer vision, machine learning, ROS2, and flight control**.

Development progresses incrementally from hardware integration and telemetry, through real-time perception, toward closed-loop autonomous target tracking and navigation.
