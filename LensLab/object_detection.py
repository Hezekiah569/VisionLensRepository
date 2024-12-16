import cv2
from ultralytics import YOLO

def detect_objects(frame, model):
    """
    Perform object detection on a given frame using the YOLO model.

    Args:
        frame: The image frame to process.
        model: The YOLO model used for detection.

    Returns:
        detected_objects: A list of detected objects with class and bounding box info.
        annotated_frame: The frame annotated with detection results.
    """
    # Perform inference
    results = model(frame)
    detected_objects = []

    for result in results:
        for box in result.boxes:
            detected_objects.append({
                'class': int(box.cls[0]),
                'bbox': box.xyxy[0].tolist()
            })

    # Annotate the frame
    annotated_frame = results[0].plot()

    return detected_objects, annotated_frame
