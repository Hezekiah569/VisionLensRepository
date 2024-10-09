import cv2
from ultralytics import YOLO

def detect_objects():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # You can also try 'yolov8s.pt' for more accuracy but lower speed

    cap = cv2.VideoCapture(0)  # Open camera

    # Optional: Set camera resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Inference using YOLOv8
        results = model(frame)

        for result in results:
            # Filter detections by confidence threshold
            if result.conf > 0.5:
                print(f"Detected: {result.name} with confidence {result.conf}")

        # Render results on the frame
        results.render()

        # Show the frame with detections
        cv2.imshow('YOLOv8 Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
