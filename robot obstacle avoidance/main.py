import cv2
import numpy as np
from ultralytics import YOLO

# Load fast lightweight detector
model = YOLO('yolov8n.pt')

def process_obstacle_zones(frame, results):
    """
    Analyzes detected objects, checks proximity to danger zones,
    and returns real-time steering decision commands.
    """
    h, w, _ = frame.shape
    
    # Define Safety Zones relative to screen frame
    # Center Danger Corridor (where the robot is driving towards)
    danger_y = int(h * 0.45)   # Top limit of critical zone
    left_bound = int(w * 0.25)
    right_bound = int(w * 0.75)

    obstacle_center = False
    obstacle_left = False
    obstacle_right = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            confidence = float(box.conf[0])
            if confidence < 0.35:
                continue

            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            obj_cx = (x1 + x2) // 2
            obj_cy = (y1 + y2) // 2

            # Determine position relative to robot corridor
            is_close = y2 > danger_y

            if is_close:
                # Color code: Red = Urgent Danger, Yellow = Caution
                box_color = (0, 0, 255) if y2 > int(h * 0.70) else (0, 255, 255)

                if obj_cx < left_bound:
                    obstacle_left = True
                elif obj_cx > right_bound:
                    obstacle_right = True
                else:
                    obstacle_center = True

                # Draw Bounding Box & Centroid Dot
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.circle(frame, (obj_cx, obj_cy), 5, (0, 0, 255), -1)

                label = f"{class_name.upper()} ({confidence:.2f})"
                cv2.putText(frame, label, (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

    # Robot Steering Decision Logic
    if obstacle_center:
        if not obstacle_left:
            command = "OBSTACLE AHEAD -> STEER LEFT"
            cmd_color = (0, 165, 255)  # Orange
        elif not obstacle_right:
            command = "OBSTACLE AHEAD -> STEER RIGHT"
            cmd_color = (0, 165, 255)  # Orange
        else:
            command = "EMERGENCY STOP - PATH BLOCKED!"
            cmd_color = (0, 0, 255)    # Red
    else:
        command = "PATH CLEAR - MOVING FORWARD"
        cmd_color = (0, 255, 0)        # Green

    return command, cmd_color, (danger_y, left_bound, right_bound)

# Open Camera
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

print("Autonomous Robot Obstacle Avoidance System Running.")
print("Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # Run YOLO Detection
    results = model(frame, stream=True, verbose=False)

    # Process obstacles and get navigation command
    command, cmd_color, (danger_y, left_bound, right_bound) = process_obstacle_zones(frame, results)

    # --- Overlay Navigation HUD ---
    # Corridor Guide Lines
    cv2.line(frame, (left_bound, 0), (left_bound, h), (100, 100, 100), 1, cv2.LINE_AA)
    cv2.line(frame, (right_bound, 0), (right_bound, h), (100, 100, 100), 1, cv2.LINE_AA)
    cv2.line(frame, (0, danger_y), (w, danger_y), (0, 255, 255), 1, cv2.LINE_AA)

    # Steering Command Top Banner
    cv2.rectangle(frame, (0, 0), (w, 60), (20, 20, 20), -1)
    cv2.putText(frame, f"NAV COMMAND: {command}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, cmd_color, 2, cv2.LINE_AA)

    cv2.imshow("Autonomous Obstacle Detection & Avoidance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()