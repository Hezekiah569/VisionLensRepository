import cv2
import time
import threading
import numpy as np
from LensLab.voice_assistance import (
    provide_voice_feedback,
    recognize_command,
    handle_command,
    speak_text,
)
from LensLab.object_detection import detect_objects
from ultralytics import YOLO
from dotenv import load_dotenv
import speech_recognition as sr
from LensLab.vibration_feedback import start_vibration_feedback, stop_vibration

load_dotenv()

# Global flags and objects
vibration_thread = None
stop_vibration_event = threading.Event()

def voice_feedback(detected_objects, model_names, image_width, image_height, mode):
    """Provide voice feedback directly (no new thread for every feedback)."""
    provide_voice_feedback(detected_objects, model_names, image_width, image_height, mode)

def speech_recognition_loop(recognizer, microphone, state_lock, state):
    """Continuous speech recognition in a thread."""
    global vibration_thread
    while True:
        try:
            command = recognize_command(recognizer, microphone)
            if command:
                with state_lock:
                    was_navigating = state["is_navigating"]
                    state["is_navigating"], state["is_identifying"] = handle_command(
                        command,
                        state["is_navigating"],
                        state["is_identifying"]
                    )

                    if state["is_navigating"] and not was_navigating:
                        print("Starting vibration...")
                        stop_vibration_event.clear()
                        vibration_thread = threading.Thread(target=start_vibration_feedback, daemon=True)
                        vibration_thread.start()

                    if not state["is_navigating"] and was_navigating:
                        print("Stopping vibration...")
                        stop_vibration_event.set()

        except Exception as e:
            print(f"[Speech Recognition Error] {e}")

def main():
    global vibration_thread
    try:
        state_lock = threading.Lock()
        state = {"is_navigating": False, "is_identifying": False}

        frame_skip = 5
        frame_count = 0
        last_feedback_time = 0
        feedback_cooldown = 3  # seconds

        # Load models
        main_model = YOLO('DP2-latest-640.onnx', task="segment")
        second_model = YOLO('yolov8n-seg.onnx')  # <-- your second model
        print("[Init] Models loaded.")

        # Initialize video capture
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Could not open video capture device")

        # Initialize speech recognizer
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        # Greet
        greeting = ( "Hi, my name's Samantha, and I will be your VisionAssistant for today. "
            "To start navigation, please say 'navigate'. To start identifying objects, say 'identify'."
            "To learn more, say 'tutorial' for a quick tutorial on how to use the system.")
        print(greeting)
        speak_text(greeting)

        # Start speech recognition in background
        threading.Thread(
            target=speech_recognition_loop,
            args=(recognizer, microphone, state_lock, state),
            daemon=True
        ).start()

        # FPS calculation
        prev_time = time.time()
        smoothed_fps = 0
        fps_alpha = 0.9

        print("[System] Ready.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Error] Failed to grab frame")
                break

            frame_count += 1

            # FPS computation
            curr_time = time.time()
            time_diff = curr_time - prev_time
            fps = 1 / time_diff if time_diff > 0 else 0
            smoothed_fps = fps_alpha * smoothed_fps + (1 - fps_alpha) * fps
            prev_time = curr_time

            # Overlay FPS
            fps_text = f"FPS: {smoothed_fps:.2f}"
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            # Check modes
            with state_lock:
                navigating = state["is_navigating"]
                identifying = state["is_identifying"]

            if (navigating or identifying) and frame_count % frame_skip == 0:
                image_height, image_width = frame.shape[:2]
                detected_objects, annotated_frame = detect_objects(frame, main_model)

                ## NEW BLOCK: Second model detections
                second_results = second_model(frame)[0]
                for box in second_results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = box
                    if int(class_id) in [0, 56]:  # Only people and chairs
                        label = "people" if int(class_id) == 0 else "chair"

                        # Draw the detection
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                        cv2.putText(annotated_frame, label, (int(x1), int(y1) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                        # ?? Add detection for voice feedback
                        detected_objects.append({
                            'name': label,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(score)
                        })


                if detected_objects and (curr_time - last_feedback_time >= feedback_cooldown):
                    mode = "navigate" if navigating else "identify"
                    voice_feedback(detected_objects, main_model.names, image_width, image_height, mode)
                    last_feedback_time = curr_time

                cv2.putText(annotated_frame, fps_text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Smart Eyewear', annotated_frame)
            else:
                cv2.imshow('Smart Eyewear', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[System] Quit signal received.")
                break
    except Exception as e:
        print(f"[Exception] {str(e)}")
    finally:
        print("[System] Cleaning up...")
        stop_vibration_event.set()
        if vibration_thread and vibration_thread.is_alive():
            vibration_thread.join()
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print("[System] Shutdown complete.")

if __name__ == "__main__":
    main()
