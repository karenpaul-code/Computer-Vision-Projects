# AI Plant Leaf Segmentation and Area Analysis System

## Project Title
Vision Based Plant Leaf Detection and Surface Area Measurement System

## Problem Statement
Automated agricultural monitoring and crop health inspection systems require non-destructive computer vision techniques to detect plant foliage, segment individual leaves, and measure leaf surface area for growth tracking and disease assessment.

## Objective
To build a computer vision pipeline using HSV color space segmentation, morphological filtering, and contour moment calculations to isolate plant leaves, determine leaf centroids, count individual foliage instances, and calculate total surface area.

## Dataset
- Input Feed: High-resolution RGB leaf images and synthetic foliage matrices processed at 800x600 resolution.

## Methodology
1. Image Preprocessing: Captures or generates the image frame and converts it to HSV color space for lighting-invariant color segmentation.
2. Color Thresholding: Defines HSV boundaries for plant green hues (Hue: 25-85, Saturation: 40-255, Value: 40-255) to create a binary mask isolating foliage from backgrounds.
3. Morphological Cleaning: Applies an ellipse structuring element opening operation (`cv2.MORPH_OPEN`) to eliminate background speckle noise.
4. Contour Analysis & Area Extraction: Detects external contours using `cv2.findContours` and filters out small noise particles ($Area < 1000 \text{ pixels}$).
5. Spatial Moments & HUD Display: Computes spatial moments ($M_{10}/M_{00}, M_{01}/M_{00}$) to locate leaf centroids, draws green boundary outlines, and overlays a live status dashboard displaying total leaf count and surface area.

## Tools and Libraries Used
- Python 3.14
- OpenCV (`cv2`)
- NumPy

## Results
The system successfully segments leaves from background surfaces, draws green boundary contours, marks center points, and displays accurate surface area measurements in real time.

## Performance Evaluation
- Processing Speed: Under 10 milliseconds execution time.
- Accuracy: High segmentation accuracy for distinct green foliage.

## Conclusion
HSV color space segmentation combined with contour moment analysis provides an effective, lightweight pipeline for automated plant growth monitoring and leaf area quantification.