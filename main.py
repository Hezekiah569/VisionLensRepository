import cv2
import time
import threading
from LensLab.voice_assistance import provide_voice_feedback, recognize_command, handle_command, speak_text
from LensLab.object_detection import detect_objects
from ultralytics import YOLO
from dotenv import load_dotenv
import speech_recognition as sr

# Load environment variables
load_dotenv()

def voice_feedback_thread(detected_objects, model_names, image_width, image_height):
    """Function to run voice feedback in a separate thread."""
    provide_voice_feedback(detected_objects, model_names, image_width, image_height)

def speech_recognition_thread(recognizer, microphone, state_lock, state):
    """Thread to continuously listen for user commands."""
    while True:
        try:
            command = recognize_command(recognizer, microphone)  # Recognize user command
            if command:
                with state_lock:
                    # Update navigation state based on command
                    state["is_navigating"] = handle_command(command, state["is_navigating"])
        except Exception as e:
            print(f"Error in recognizing command: {e}")

def main():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)

    # Initialize recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Variables to calculate FPS and track greeting state
    prev_time = 0
    greeting_state = {'greeting_given': False}

    # Shared state for threading
    state = {"is_navigating": False}
    state_lock = threading.Lock()

    # Initial Greeting
    initial_greeting = (
        "Hi, my name's Samantha, and I will be your VisionAssistant for today. "
        "To start navigation, please say 'navigate'."
    )
    print(initial_greeting)
    speak_text(initial_greeting)  # Issue the greeting before entering the main loop

    # Start the speech recognition thread
    threading.Thread(target=speech_recognition_thread, args=(recognizer, microphone, state_lock, state), daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Read navigation state safely
        with state_lock:
            is_navigating = state["is_navigating"]

        if is_navigating:
            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            image_height, image_width = frame.shape[:2]

            # Perform object detection
            detected_objects, annotated_frame = detect_objects(frame, model)

            # Start voice feedback in a separate thread
            voice_thread = threading.Thread(
                target=voice_feedback_thread,
                args=(detected_objects, model.names, image_width, image_height),
            )
            voice_thread.start()

            # Display FPS on the frame
            cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show the annotated frame
            cv2.imshow('Smart Eyewear', annotated_frame)
        else:
            # Display the frame while idle (waiting for commands)
            cv2.imshow('Smart Eyewear', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
