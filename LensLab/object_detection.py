import cv2
from ultralytics import YOLO

def detect_objects(frame, model, confidence_threshold=0.75):
    """
    Perform object detection on a given frame using the YOLO model.

    Args:
        frame: The image frame to process.
        model: The YOLO model used for detection.
        confidence_threshold: Minimum confidence score for an object to be considered valid.

    Returns:
        detected_objects: A list of detected objects with class, bounding box info, and confidence scores.
        annotated_frame: The frame annotated with detection results.
    """
    # Perform inference
    results = model(frame)
    detected_objects = []

    for result in results:
        for box in result.boxes:
            confidence = float(box.conf[0])
            if confidence >= confidence_threshold:
                detected_objects.append({
                    'class': int(box.cls[0]),
                    'bbox': box.xyxy[0].tolist(),
                    'confidence': confidence
                })

    # Annotate the frame
    annotated_frame = results[0].plot()

    return detected_objects, annotated_frame
