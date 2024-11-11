import cv2
from ultralytics import YOLO

def detect_objects(frame, model):
    # Perform detection using YOLOv8
    results = model(frame)

    # Extract detection details and annotate the frame
    detected_objects = []
    for r in results:  # Iterate over the results
        boxes = r.boxes  # Get detected boxes
        for box in boxes:
            cls = int(box.cls)  # Get class index
            conf = float(box.conf)  # Get confidence score
            bbox = box.xyxy[0].tolist()  # Get bounding box coordinates as [x1, y1, x2, y2]

            # Apply confidence threshold
            if conf > 0.5:
                detected_objects.append({
                    'class': cls,
                    'confidence': conf,
                    'bbox': bbox  # Pass bounding box for positional feedback
                })

    # Annotate the frame with detection results
    annotated_frame = results[0].plot()  # This plots bounding boxes and labels on the frame

    return detected_objects, annotated_frame
