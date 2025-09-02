import cv2
import numpy as np
import time
from object_values import get_object_value

# Load YOLO
yolo = cv2.dnn.readNet("yolov3-custom_final.weights", "yolov3-tiny.cfg")
yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load class labels
with open("coco.names", "r") as file:
    classes = [line.strip() for line in file.readlines()]

# Define classes to ignore
ignore_classes = ["person", "car", "truck", "bus", "motorbike", "bicycle", "dining table", "chair"]
ignore_ids = [classes.index(cls) for cls in ignore_classes if cls in classes]

# Get YOLO output layers
layer_names = yolo.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo.getUnconnectedOutLayers().flatten()]

# Define colors for each value (1-4)
value_colors = {
    1: (0, 255, 0),     # Green
    2: (0, 255, 255),   # Yellow
    3: (0, 165, 255),   # Orange
    4: (0, 0, 255)      # Red
}

# Default color for debugging
colorCyan = (255, 255, 0)

# Function to check if two rectangles intersect
def rectangles_intersect(rect1, rect2):
    # rect format: [x, y, w, h]
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    # Check if one rectangle is to the left of the other
    if x1 + w1 < x2 or x2 + w2 < x1:
        return False
    
    # Check if one rectangle is above the other
    if y1 + h1 < y2 or y2 + h2 < y1:
        return False
    
    # If neither of the above, they must intersect
    return True

# Start video capture
cap = cv2.VideoCapture(0)
prev_time = 0

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.resize(img, (640, 480))
    height, width, _ = img.shape

    # ---------------- YOLO Object Detection ----------------
    blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    yolo.setInput(blob)
    outputs = yolo.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Store the valid object boxes
    object_boxes = []
    object_labels = []
    for i in range(len(boxes)):
        if i in indexes:
            class_id = class_ids[i]
            if class_id in ignore_ids:
                continue  # Skip ignored classes
            object_boxes.append(boxes[i])
            object_labels.append(classes[class_id])

    # ---------------- Green Arm Detection ----------------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Wider green range (adjust based on lighting)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Morphology to remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Store all arm bounding boxes with significant area
    arm_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:  # smaller threshold to catch farther arms
            x, y, w, h = cv2.boundingRect(cnt)
            arm_boxes.append([x, y, w, h])

    # ---------------- Detect Interactions and Show Values ----------------
    interactions = []
    
    for obj_idx, obj_box in enumerate(object_boxes):
        for arm_box in arm_boxes:
            if rectangles_intersect(obj_box, arm_box):
                label = object_labels[obj_idx]
                
                # Get the value (1-4) for this object
                value = get_object_value(label)
                
                # Get the color associated with this value
                color = value_colors[value]
                
                # Draw the object with value-specific color
                x, y, w, h = obj_box
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                
                # Display object name and value
                cv2.putText(img, f"{label}: {value}", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                # Add to interactions list
                interactions.append((obj_box, label, value))
                break

    # ---------------- FPS Display ----------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colorCyan, 2)
    
    # Show count of detected interactions
    cv2.putText(img, f'Interactions: {len(interactions)}', (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorCyan, 2)

    # ---------------- Show Result ----------------
    cv2.imshow("Object-Arm Interaction with Values", img)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()