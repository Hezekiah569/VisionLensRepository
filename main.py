import cv2
import time
import threading
from LensLab.voice_assistance import provide_voice_feedback  # Import the updated function
from LensLab.object_detection import detect_objects  # Import the detect_objects function
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

def voice_feedback_thread(detected_objects, model_names, image_width, image_height, greeting_state):
    """Function to run voice feedback in a separate thread."""
    provide_voice_feedback(detected_objects, model_names, image_width, image_height, greeting_state)

def main():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    # Variables to calculate FPS and control feedback timing
    prev_time = 0
    last_feedback_time = time.time()  # Tracks the last time feedback was given
    feedback_cooldown = 5  # Cooldown period in seconds for giving feedback

    # Initialize greeting_state to track if greeting was given
    greeting_state = {'greeting_given': False}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get current time to calculate FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        # Get frame dimensions for voice feedback
        image_height, image_width = frame.shape[:2]

        # Perform detection using the imported detect_objects function
        detected_objects, annotated_frame = detect_objects(frame, model)  # Pass the model here

        # Check if enough time has passed since the last feedback
        if time.time() - last_feedback_time > feedback_cooldown:
            if not greeting_state['greeting_given']:
                # Run the greeting in the voice feedback thread
                voice_thread = threading.Thread(target=voice_feedback_thread, args=([], model.names, image_width, image_height, greeting_state))
                voice_thread.start()
                greeting_state['greeting_given'] = True  # Update the state to reflect that greeting has been given
                last_feedback_time = time.time()  # Reset the feedback timer
            elif detected_objects:
                # Run the feedback for detected objects in a separate thread
                voice_thread = threading.Thread(target=voice_feedback_thread, args=(detected_objects, model.names, image_width, image_height, greeting_state))
                voice_thread.start()
                last_feedback_time = time.time()  # Reset the feedback timer

        # Display FPS on the frame
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame with results and FPS
        cv2.imshow('Smart Eyewear', annotated_frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
