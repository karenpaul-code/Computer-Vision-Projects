import cv2
import numpy as np

# Grid state: False = Green (EMPTY), True = Red (OCCUPIED / CAR PRESENT)
grid_states = [False] * 9

def create_road_background(w=900, h=600):
    """Generates a grey asphalt road background with parking lane markings."""
    # Dark grey asphalt color
    bg = np.full((h, w, 3), (60, 60, 60), dtype=np.uint8)
    
    # Add subtle asphalt texture noise
    noise = np.random.randint(-10, 10, (h, w, 3), dtype=np.int16)
    bg = np.clip(bg.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Draw white dashed road lines along the grid borders
    cell_w, cell_h = w // 3, h // 3
    
    # Yellow divider lines between columns
    for col in range(1, 3):
        x = col * cell_w
        cv2.line(bg, (x, 0), (x, h), (0, 215, 255), 3)

    # White dashed lines between rows
    for row in range(1, 3):
        y = row * cell_h
        for x in range(0, w, 30):
            cv2.line(bg, (x, y), (min(x + 15, w), y), (255, 255, 255), 2)

    return bg

def draw_car(img, x1, y1, x2, y2):
    """Draws a stylized car icon inside the specified bounding box."""
    pad_x = int((x2 - x1) * 0.2)
    pad_y = int((y2 - y1) * 0.15)
    
    cx1, cy1 = x1 + pad_x, y1 + pad_y
    cx2, cy2 = x2 - pad_x, y2 - pad_y
    
    # Car Body (Red Metallic)
    cv2.rectangle(img, (cx1, cy1), (cx2, cy2), (30, 30, 200), -1)
    cv2.rectangle(img, (cx1, cy1), (cx2, cy2), (0, 0, 150), 2)
    
    # Windshield / Roof (Dark Glass)
    rx1 = cx1 + int((cx2 - cx1) * 0.2)
    ry1 = cy1 + int((cy2 - cy1) * 0.25)
    rx2 = cx2 - int((cx2 - cx1) * 0.2)
    ry2 = cy2 - int((cy2 - cy1) * 0.25)
    cv2.rectangle(img, (rx1, ry1), (rx2, ry2), (180, 130, 70), -1)
    
    # Wheels (Black Rectangles on sides)
    wheel_w = int((cx2 - cx1) * 0.1)
    wheel_h = int((cy2 - cy1) * 0.2)
    
    # Top-Left, Bottom-Left, Top-Right, Bottom-Right wheels
    cv2.rectangle(img, (cx1 - wheel_w, cy1 + 5), (cx1, cy1 + 5 + wheel_h), (20, 20, 20), -1)
    cv2.rectangle(img, (cx1 - wheel_w, cy2 - 5 - wheel_h), (cx1, cy2 - 5), (20, 20, 20), -1)
    cv2.rectangle(img, (cx2, cy1 + 5), (cx2 + wheel_w, cy1 + 5 + wheel_h), (20, 20, 20), -1)
    cv2.rectangle(img, (cx2, cy2 - 5 - wheel_h), (cx2 + wheel_w, cy2 - 5), (20, 20, 20), -1)

def mouse_click(event, x, y, flags, param):
    """Detect mouse clicks to toggle grid cell state."""
    if event == cv2.EVENT_LBUTTONDOWN:
        frame_w, frame_h = param['width'], param['height']
        cell_w = frame_w // 3
        cell_h = frame_h // 3
        
        col = min(x // cell_w, 2)
        row = min(y // cell_h, 2)
        index = row * 3 + col
        
        # Toggle spot occupancy
        grid_states[index] = not grid_states[index]

# Dimensions
WIDTH, HEIGHT = 900, 600
road_bg = create_road_background(WIDTH, HEIGHT)

cv2.namedWindow("3x3 Parking Road Grid")

print("Interactive 3x3 Road Parking Active.")
print("Click any spot to park/remove a car. Press 'q' to exit.")

while True:
    # Copy clean asphalt background frame
    frame = road_bg.copy()
    cell_w, cell_h = WIDTH // 3, HEIGHT // 3

    cv2.setMouseCallback("3x3 Parking Road Grid", mouse_click, {'width': WIDTH, 'height': HEIGHT})

    occupied_count = sum(grid_states)
    free_spots = 9 - occupied_count

    # Render Grid and Cars
    for i in range(9):
        row = i // 3
        col = i % 3
        
        x1, y1 = col * cell_w, row * cell_h
        x2, y2 = x1 + cell_w, y1 + cell_h
        
        is_occupied = grid_states[i]
        
        if is_occupied:
            # Draw Car inside spot and outline in Red
            draw_car(frame, x1, y1, x2, y2)
            cv2.rectangle(frame, (x1 + 5, y1 + 5), (x2 - 5, y2 - 5), (0, 0, 255), 3)
            status_text = f"P{i+1}: OCCUPIED"
            text_color = (0, 0, 255)
        else:
            # Empty Spot outline in Green
            cv2.rectangle(frame, (x1 + 5, y1 + 5), (x2 - 5, y2 - 5), (0, 255, 0), 2)
            status_text = f"P{i+1}: EMPTY"
            text_color = (0, 255, 0)

        # Label Spot
        cv2.putText(frame, status_text, (x1 + 15, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, text_color, 2, cv2.LINE_AA)

    # Top Status Bar Overlay
    if free_spots == 0:
        cv2.rectangle(frame, (20, 10), (460, 65), (0, 0, 200), -1)
        cv2.putText(frame, "PARKING FULL!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3, cv2.LINE_AA)
    else:
        cv2.rectangle(frame, (20, 10), (460, 65), (0, 0, 0), -1)
        cv2.putText(frame, f"Spots Remaining: {free_spots} / 9", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("3x3 Parking Road Grid", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()