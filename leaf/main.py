import cv2
import numpy as np

def create_synthetic_leaf_sample(w=800, h=600):
    """Generates a clean test image with green plant leaves on a wooden background."""
    # Background: Light brown wooden surface
    canvas = np.full((h, w, 3), (120, 160, 200), dtype=np.uint8)
    
    # Draw Leaf 1 (Large Center Leaf)
    pts1 = np.array([[300, 200], [450, 150], [550, 300], [450, 450], [300, 400], [250, 300]], np.int32)
    cv2.fillPoly(canvas, [pts1], (30, 140, 40))   # Green leaf color
    cv2.polylines(canvas, [pts1], True, (20, 100, 30), 3)

    # Draw Leaf 2 (Smaller Side Leaf)
    pts2 = np.array([[120, 100], [220, 80], [280, 180], [200, 260], [110, 200]], np.int32)
    cv2.fillPoly(canvas, [pts2], (40, 160, 50))
    
    # Add stem lines
    cv2.line(canvas, (300, 300), (200, 480), (10, 80, 20), 6)
    cv2.line(canvas, (180, 170), (100, 280), (10, 80, 20), 4)
    
    return canvas

def analyze_plant_leaves():
    # Generate test image
    frame = create_synthetic_leaf_sample()
    h, w, _ = frame.shape

    # Convert to HSV color space for accurate green isolation
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define Green Color Range (HSV)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])

    # Create Binary Mask for Leaves
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Morphological noise removal
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find Leaf Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    leaf_count = 0
    total_surface_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Filter small noise pixels
            leaf_count += 1
            total_surface_area += area

            # Draw green bounding contour outline around leaf
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 3)

            # Compute centroid for text labeling
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Draw centroid red dot
                cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
                
                # Label Leaf ID and Area in pixels
                label = f"Leaf #{leaf_count} ({int(area)} px)"
                cv2.putText(frame, label, (cx - 60, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    # HUD Banner Overlay
    cv2.rectangle(frame, (0, 0), (w, 60), (20, 20, 20), -1)
    status_text = f"DETECTED LEAVES: {leaf_count} | TOTAL AREA: {int(total_surface_area)} sq.px"
    cv2.putText(frame, status_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    print("\n[SUCCESS] Leaf Detection Complete!")
    print(f"Leaves Detected: {leaf_count}")
    print(f"Total Surface Area: {int(total_surface_area)} pixels\n")

    cv2.imshow("AI Plant Leaf Segmentation & Area Analysis", frame)
    cv2.waitKey(0)  # Keeps window open until key press
    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyze_plant_leaves()