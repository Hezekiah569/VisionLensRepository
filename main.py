import cv2
import time
import threading
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

load_dotenv()


def voice_feedback_thread(detected_objects, model_names, image_width, image_height, mode):
    provide_voice_feedback(detected_objects, model_names, image_width, image_height, mode)


def speech_recognition_thread(recognizer, microphone, state_lock, state):
    while True:
        try:
            command = recognize_command(recognizer, microphone)
            if command:
                with state_lock:
                    state["is_navigating"], state["is_identifying"] = handle_command(
                        command,
                        state["is_navigating"],
                        state["is_identifying"]
                    )
        except Exception as e:
            print(f"Error in recognizing command: {e}")


def main():
    try:
        state_lock = threading.Lock()
        state = {"is_navigating": False, "is_identifying": False}
        last_feedback_time = 0
        feedback_cooldown = 5
        min_objects_for_feedback = 1

        frame_skip = 10
        frame_count = 0

        model = YOLO('DP1.onnx', task="segment")

        print("Initializing video capture...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Could not open video capture device")

        print("Initializing speech recognition...")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        initial_greeting = (
            "Hi, my name's Samantha, and I will be your VisionAssistant for today. "
            "To start navigation, please say 'navigate'. To start identifying objects, say 'identify'."
            "To learn more, say 'tutorial' for a quick tutorial on how to use the system."
        )
        print(initial_greeting)
        speak_text(initial_greeting)

        print("Starting speech recognition thread...")
        threading.Thread(
            target=speech_recognition_thread,
            args=(recognizer, microphone, state_lock, state),
            daemon=True
        ).start()

        prev_time = time.time()
        fps_alpha = 0.9
        smoothed_fps = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame_count += 1

            curr_time = time.time()
            time_diff = curr_time - prev_time
            instantaneous_fps = 1 / time_diff if time_diff > 0 else 0
            smoothed_fps = (fps_alpha * smoothed_fps +
                            (1 - fps_alpha) * instantaneous_fps)
            prev_time = curr_time

            fps_text = f"FPS: {smoothed_fps:.2f}"
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            with state_lock:
                is_navigating = state["is_navigating"]
                is_identifying = state["is_identifying"]

            if (is_navigating or is_identifying) and frame_count % frame_skip == 0:
                image_height, image_width = frame.shape[:2]
                detected_objects, annotated_frame = detect_objects(frame, model)

                if (len(detected_objects) >= min_objects_for_feedback and
                        (curr_time - last_feedback_time) >= feedback_cooldown):
                    mode = "navigate" if is_navigating else "identify"
                    voice_thread = threading.Thread(
                        target=voice_feedback_thread,
                        args=(detected_objects, model.names, image_width, image_height, mode)
                    )
                    voice_thread.start()
                    last_feedback_time = curr_time

                cv2.putText(annotated_frame, fps_text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Smart Eyewear', annotated_frame)
            else:
                cv2.imshow('Smart Eyewear', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit command received")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Cleaning up...")
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        print("System shutdown complete")


if __name__ == "__main__":
    main()