import cv2
from ultralytics import YOLO
def detect_objects(frame, model, confidence_threshold=0.5):
    try:
        results = model(frame)[0]
        detected_objects = []
        for box in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = box
            if score >= confidence_threshold:
                class_name = model.names[int(class_id)]
                detected_objects.append({
                    'class': int(class_id),
                    'class_name': class_name,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': score
                })
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                label = f"{class_name.upper()} {score:.2f}"
                cv2.putText(frame,
                            label,
                            (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 255, 0),
                            2,
                            cv2.LINE_AA)
        return detected_objects, frame
    except Exception as e:
        print(f"Error in object detection: {str(e)}")
        return [], frame
