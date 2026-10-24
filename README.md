# Computer Vision and Robotics Project Portfolio

This repository contains five computer vision applications developed in Python using OpenCV, YOLOv8, and NumPy.

## Project Directory

1. 01_Traffic_Sign_Detection: Real-time traffic sign detection and classification using YOLOv8 and HSV color filtering.
2. 02_Parking_Slot_Occupancy: Interactive 3x3 road grid parking space occupancy monitoring system.
3. 03_Robotic_Pick_and_Place: Target localization, coordinate conversion, and 2D virtual robotic arm simulation.
4. 04_Autonomous_Self_Parking: Trajectory planning and Bezier curve steering simulation for autonomous self-parking.
5. 05_Obstacle_Avoidance: Real-time obstacle detection, corridor zone mapping, and navigation steering decisions.

## Requirements

Install all necessary packages across all projects using:
pip install opencv-python ultralytics numpy pyserial

## How to Run

Navigate into any project folder and run its corresponding Python script:

1. Traffic Sign Detection:
   cd 01_Traffic_Sign_Detection
   python main.py

2. Parking Occupancy:
   cd 02_Parking_Slot_Occupancy
   python parking.py

3. Robotic Pick and Place:
   cd 03_Robotic_Pick_and_Place
   python pick_and_place.py

4. Autonomous Self Parking:
   cd 04_Autonomous_Self_Parking
   python autonomous.py

5. Obstacle Avoidance:
   cd 05_Obstacle_Avoidance
   python obstacle_detection.py