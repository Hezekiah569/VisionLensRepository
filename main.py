import cv2
from LensLab.voice_assistance import provide_voice_feedback  # Import the voice feedback function
from ultralytics import YOLO

def main():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # You can choose 'yolov8n.pt', 'yolov8s.pt', etc. depending on your needs
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection using YOLOv8
        results = model(frame)

        # Extract detection details
        detected_objects = []
        for r in results:  # Iterate over the results
            boxes = r.boxes  # Get detected boxes
            for box in boxes:
                cls = int(box.cls)  # Get class index
                conf = float(box.conf)  # Get confidence score

                # Apply confidence threshold
                if conf > 0.5:
                    detected_objects.append({
                        'class': cls,
                        'confidence': conf
                    })

        # Provide voice feedback for detected objects, pass class names
        provide_voice_feedback(detected_objects, model.names)

        # Render the results on the frame
        annotated_frame = r.plot()  # This plots bounding boxes and labels on the frame

        # Display the frame with results
        cv2.imshow('Smart Eyewear', annotated_frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
