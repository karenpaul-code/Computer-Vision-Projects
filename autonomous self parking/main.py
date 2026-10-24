import cv2
import numpy as np
import math

class AutonomousParkingSim:
    def __init__(self, width=900, height=600):
        self.w = width
        self.h = height
        
        # Target Parking Slot (Center X, Center Y, Width, Height)
        self.target_slot = [650, 450, 140, 220]
        
        # Vehicle State
        self.reset_vehicle()

    def reset_vehicle(self):
        """Resets car back to starting road position."""
        self.car_x = 150.0
        self.car_y = 180.0
        self.car_angle = 0.0  # Facing right (0 deg)
        self.is_parking = False
        self.parked = False
        self.path = []

    def plan_parking_trajectory(self):
        """Generates trajectory path points for reverse bay parking into target slot."""
        tx, ty, tw, th = self.target_slot
        
        # Key Waypoints: [Start] -> [Alignment Point] -> [Reverse Curve] -> [Final Slot Center]
        align_x, align_y = tx - 80, ty - 220
        entry_x, entry_y = tx, ty - 120
        final_x, final_y = tx, ty
        
        waypoints = []
        
        # Stage 1: Drive forward to alignment position
        for t in np.linspace(0, 1, 30):
            x = self.car_x + t * (align_x - self.car_x)
            y = self.car_y + t * (align_y - self.car_y)
            waypoints.append((x, y, 0))

        # Stage 2: Reverse curve into slot entry
        for t in np.linspace(0, 1, 40):
            # Quadratic Bezier curve for smooth steering maneuver
            x = (1-t)**2 * align_x + 2*(1-t)*t * entry_x + t**2 * final_x
            y = (1-t)**2 * align_y + 2*(1-t)*t * entry_y + t**2 * final_y
            angle = 90 * t  # Rotate towards vertical slot alignment
            waypoints.append((x, y, angle))

        self.path = waypoints

    def update_vehicle_kinematics(self):
        """Updates autonomous car along calculated trajectory."""
        if not self.is_parking or not self.path:
            return

        if len(self.path) > 0:
            target_x, target_y, target_angle = self.path.pop(0)
            self.car_x = target_x
            self.car_y = target_y
            self.car_angle = target_angle
        else:
            self.parked = True

    def draw_environment(self):
        """Renders road, parking bays, vision lines, and car."""
        # Dark Asphalt Background
        frame = np.full((self.h, self.w, 3), (50, 50, 50), dtype=np.uint8)

        # Draw Road Markings
        cv2.line(frame, (0, 260), (self.w, 260), (255, 255, 255), 3)
        for x in range(0, self.w, 40):
            cv2.line(frame, (x, 130), (x + 20, 130), (0, 215, 255), 2)

        # Parking Bays
        slots = [
            (250, 450, True),   # Occupied
            (450, 450, True),   # Occupied
            (650, 450, False),  # Target Free Slot
        ]

        for sx, sy, occupied in slots:
            sw, sh = 140, 220
            x1, y1 = sx - sw//2, sy - sh//2
            x2, y2 = sx + sw//2, sy + sh//2
            
            color = (0, 0, 255) if occupied else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            if occupied:
                cv2.rectangle(frame, (x1 + 15, y1 + 20), (x2 - 15, y2 - 20), (120, 120, 120), -1)
                cv2.putText(frame, "OCCUPIED", (x1 + 15, sy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(frame, "TARGET SLOT", (x1 + 10, sy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw Trajectory Path
        if self.path:
            for i in range(len(self.path) - 1):
                p1 = (int(self.path[i][0]), int(self.path[i][1]))
                p2 = (int(self.path[i+1][0]), int(self.path[i+1][1]))
                cv2.line(frame, p1, p2, (255, 255, 0), 2, cv2.LINE_AA)

        # Draw Autonomous Car
        car_w, car_h = 60, 110
        rect = ((self.car_x, self.car_y), (car_w, car_h), self.car_angle)
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        
        cv2.drawContours(frame, [box], 0, (0, 200, 255), -1)
        cv2.drawContours(frame, [box], 0, (255, 255, 255), 2)

        # Direction Indicator / Headlight point
        rad = math.radians(self.car_angle)
        hx = int(self.car_x + math.sin(rad) * 40)
        hy = int(self.car_y - math.cos(rad) * 40)
        cv2.circle(frame, (hx, hy), 6, (0, 255, 255), -1)

        # Dashboard Overlay
        cv2.rectangle(frame, (15, 15), (500, 75), (0, 0, 0), -1)
        
        if self.parked:
            status = "AUTONOMOUS PARKING COMPLETE!"
            color = (0, 255, 0)
        elif self.is_parking:
            status = "AUTONOMOUS PARKING IN PROGRESS..."
            color = (0, 255, 255)
        else:
            status = "PRESS 'SPACE' TO START AUTONOMOUS PARKING"
            color = (255, 255, 255)

        cv2.putText(frame, status, (25, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2, cv2.LINE_AA)
        
        cv2.putText(frame, "Press 'r' to Reset | 'q' to Quit", (25, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        return frame

# Main Program Execution
sim = AutonomousParkingSim()
cv2.namedWindow("Autonomous Vision-Based Parking System")

print("Autonomous Parking System Active.")
print("Press SPACEBAR to start auto-parking. Press 'r' to reset.")

while True:
    sim.update_vehicle_kinematics()
    frame = sim.draw_environment()

    cv2.imshow("Autonomous Vision-Based Parking System", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break
    elif key == 32:  # Spacebar key
        if not sim.is_parking and not sim.parked:
            sim.plan_parking_trajectory()
            sim.is_parking = True
    elif key == ord('r'):
        sim.reset_vehicle()

cv2.destroyAllWindows()