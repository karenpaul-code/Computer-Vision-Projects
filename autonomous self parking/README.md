# Vision Based Autonomous Self Parking System

## Project Title
Trajectory Planning and Motion Simulation for Autonomous Self Parking Systems

## Problem Statement
Autonomous vehicle self-parking requires precise path planning maneuvers in tight spaces where standard linear pathfinding fails to align the vehicle within parking slot boundaries.

## Objective
To design and simulate an autonomous self-parking path-planning agent that computes Quadratic Bezier trajectory curves to execute smooth reverse bay parking maneuvers into designated parking slots.

## Dataset
- Simulation Canvas: 900x600 pixel road environment featuring occupied bays, target vacant slots, and road lane boundaries generated dynamically in Python.

## Methodology
1. Vehicle State Vector: Tracks ego vehicle position coordinates (X, Y) and orientation angle in degrees.
2. Trajectory Calculation: Generates path waypoints upon pressing the spacebar key:
   - Approach Stage: Linear translation along the main road to reach an alignment position.
   - Reverse Stage: Quadratic Bezier curve connecting alignment point to final slot center:
     $$B(t) = (1-t)^2 P_0 + 2(1-t)t P_1 + t^2 P_2, \quad t \in [0, 1]$$
3. Steering Angle Interpolation: Gradually rotates the vehicle angle from 0 degrees to 90 degrees during slot entry.
4. Kinematic Motion Controller: Iteratively updates car position along calculated waypoints to simulate self-parking execution.

## Tools and Libraries Used
- Python 3.14
- OpenCV (cv2)
- NumPy
- Math module

## Results
The vehicle successfully plans a curved trajectory line and executes reverse bay parking into open slots while displaying state updates on a dashboard overlay.

## Performance Evaluation
- Path Calculation Time: Under 1 millisecond
- Motion Execution: Smooth animation running at 30 FPS
- Parking Accuracy: Perfect 90 degree alignment inside designated bay boundaries

## Conclusion
Quadratic Bezier curves provide a simple mathematical method for simulating smooth self-parking steering maneuvers in autonomous vehicle applications.