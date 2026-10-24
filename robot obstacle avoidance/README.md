# Autonomous Robot Obstacle Detection and Avoidance System

## Project Title
Vision Based Real Time Obstacle Detection and Steering Command System for Autonomous Robots

## Problem Statement
Mobile autonomous robots operating in unknown environments must constantly detect dynamic obstacles in their driving path and issue real-time steering commands to prevent physical collisions.

## Objective
To build a lightweight vision system using YOLOv8 object detection paired with spatial corridor zone mapping to identify close obstacles and compute automated steering decisions (Steer Left, Steer Right, Emergency Stop, or Path Clear).

## Dataset
- Model Weights: Ultralytics YOLOv8 Nano model (yolov8n.pt)
- Base Dataset: Microsoft COCO Dataset (80 general object classes including people, furniture, and vehicles)
- Real-world Validation: Live webcam video feed running at 800x600 resolution

## Methodology
1. Frame Capture: Connects to live camera stream and resizes video frames to 800x600 resolution.
2. Neural Object Detection: Passes video frames through YOLOv8n to identify surrounding objects with a confidence score threshold above 0.35.
3. Corridor Zone Division: Divides the video frame into three vertical lanes (Left, Center Corridor, Right) and sets a horizontal proximity boundary (lower 55% of screen).
4. Zone Evaluation: Checks whether bounding boxes cross the critical lower threshold line to determine if obstacles pose an immediate threat.
5. Navigation Logic: Evaluates occupied lanes to issue dynamic navigation overlay commands:
   - Path Clear -> Move Forward
   - Center Occupied (Left Free) -> Steer Left
   - Center & Left Occupied (Right Free) -> Steer Right
   - All Corridors Blocked -> Emergency Stop

## Tools and Libraries Used
- Python 3.14
- OpenCV (cv2)
- Ultralytics YOLOv8
- NumPy

## Results
The system detects real-world objects across driving corridors in real time, overlays safety guidelines, and updates navigation command banners without frame lag.

## Performance Evaluation
- Frame Rate: 30+ FPS on standard CPU hardware
- Detection Latency: Less than 25 milliseconds per frame

## Conclusion
Spatial corridor mapping combined with real-time YOLO object detection provides an efficient decision pipeline for autonomous robot navigation without needing heavy LIDAR sensors.