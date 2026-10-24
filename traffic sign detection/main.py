import cv2
import numpy as np
from ultralytics import YOLO

# Load lightweight neural detection network (runs fast on CPU)
model = YOLO('yolov8n.pt')

def categorize_sign(crop):
    """
    Lightning-fast color & shape geometric matcher (Runs in <1ms)
    """
    if crop is None or crop.size == 0 or crop.shape[0] < 25 or crop.shape[1] < 25:
        return None

    h, w, _ = crop.shape
    aspect_ratio = float(w) / h
    
    # Ignore non-square bounding boxes (like human faces, tall objects, etc.)
    if aspect_ratio < 0.7 or aspect_ratio > 1.4:
        return None

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # 1. Red Mask (Prohibitory & Stop Signs)
    r1 = cv2.inRange(hsv, np.array([0, 100, 70]), np.array([10, 255, 255]))
    r2 = cv2.inRange(hsv, np.array([160, 100, 70]), np.array([180, 255, 255]))
    mask_red = cv2.bitwise_or(r1, r2)

    # 2. White Mask
    mask_white = cv2.inRange(hsv, np.array([0, 0, 160]), np.array([180, 60, 255]))

    # 3. Blue Mask (Mandatory Signs e.g., U-Turn, Direction)
    mask_blue = cv2.inRange(hsv, np.array([95, 120, 60]), np.array([135, 255, 255]))

    total_pixels = h * w
    red_ratio = np.sum(mask_red > 0) / total_pixels
    white_ratio = np.sum(mask_white > 0) / total_pixels
    blue_ratio = np.sum(mask_blue > 0) / total_pixels

    # --- NO ENTRY SIGN CHECK ---
    # Red background circle with horizontal white line in the middle
    if red_ratio > 0.35 and white_ratio > 0.10:
        mid_y1, mid_y2 = int(h * 0.35), int(h * 0.65)
        mid_strip = mask_white[mid_y1:mid_y2, :]
        mid_white_ratio = np.sum(mid_strip > 0) / (mid_strip.size + 1e-5)
        if mid_white_ratio > 0.30:
            return "NO ENTRY"

    # --- U-TURN / MANDATORY SIGN CHECK ---
    if blue_ratio > 0.30:
        return "U-TURN / DIRECTION SIGN"

    # --- STOP SIGN ---
    if red_ratio > 0.50:
        return "STOP SIGN"

    # --- SPEED LIMIT / PROHIBITION ---
    if red_ratio > 0.20 and white_ratio > 0.25:
        return "SPEED LIMIT / PROHIBITION"

    # --- YIELD / WARNING ---
    if red_ratio > 0.15 and white_ratio > 0.40:
        return "YIELD / WARNING SIGN"

    return None


# Open webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

# Lower resolution slightly to guarantee high FPS and smooth performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Fast Real-Time Sign Detector Running! Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO with class filter to IGNORE faces, people, chairs, etc.
    # COCO Class 11 = Stop Sign, 9 = Traffic Light
    results = model(frame, conf=0.25, verbose=False)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Clip box bounds within image frame
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)

            crop = frame[y1:y2, x1:x2]

            label = None

            # Only process if detected object is a known sign or custom region
            if class_name == 'stop sign':
                label = "STOP SIGN"
            else:
                # Run fast matcher
                detected = categorize_sign(crop)
                if detected:
                    label = detected

            if label:
                # Draw Box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Banner text
                display_text = f"{label} ({confidence:.2f})"
                (tw, th), _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (x1, y1 - 25), (x1 + tw + 8, y1), (0, 255, 0), -1)
                cv2.putText(frame, display_text, (x1 + 4, y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Fast Traffic Sign Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()