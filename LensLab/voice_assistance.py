import azure.cognitiveservices.speech as speechsdk
import time  # Ensure time is imported
from dotenv import load_dotenv
import os

load_dotenv()

# Set up Azure Speech SDK configuration
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-SerenaMultilingualNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Initialize feedback tracking variables
last_feedback = {}
FEEDBACK_COOLDOWN = 5  # Cooldown period in seconds


def get_relative_position(bbox, image_width, image_height):
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2
    horizontal_position = "left" if x_center < image_width / 3 else "right" if x_center > 2 * image_width / 3 else "center"
    vertical_position = "top" if y_center < image_height / 3 else "bottom" if y_center > 2 * image_height / 3 else "middle"
    return f"{vertical_position} {horizontal_position}".strip() if horizontal_position != "center" or vertical_position != "middle" else "center"


def provide_voice_feedback(detected_objects, class_names, image_width, image_height, greeting_state):
    global last_feedback
    current_time = time.time()

    # Initial greeting
    if not greeting_state['greeting_given']:
        text = "Hi, my name's Samantha and I will be your VisionAssistant for today. Hope we get along well!"
        result = speech_synthesizer.speak_text_async(text).get()
        greeting_state['greeting_given'] = True
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesis failed for greeting.")

    feedback_parts = []
    current_feedback = {}  # Temporary storage for objects detected this frame

    # Generate feedback for detected objects
    for obj in detected_objects:
        if 'class' in obj and 'bbox' in obj:
            index = obj['class']
            if 0 <= index < len(class_names):
                object_name = class_names[index]
                position = get_relative_position(obj['bbox'], image_width, image_height)

                # Check if the object can be mentioned based on cooldown
                if (object_name not in last_feedback or
                        last_feedback[object_name]['position'] != position or
                        current_time - last_feedback[object_name]['time'] > FEEDBACK_COOLDOWN):

                    # Store current feedback for this object
                    current_feedback[object_name] = {'position': position, 'time': current_time}

                    # Custom responses based on object type
                    if object_name in ["person", "obstacle", "object"]:
                        feedback_parts.append(f"There's a {object_name} to your {position}.")
                    elif object_name in ["upstairs", "downstairs"]:
                        feedback_parts.append(f"Walk slowly, there's a {object_name} to your {position}.")
                    elif object_name == "handrail":
                        feedback_parts.append(f"Grab that handrail to your {position}.")
                    elif object_name == "wall":
                        feedback_parts.append(f"Walk slowly, there's a wall to your {position}.")

    # Update last_feedback only if there is new feedback
    if feedback_parts:
        last_feedback = current_feedback
        feedback = " ".join(feedback_parts)
    else:
        feedback = None  # No new feedback

    # Speak the feedback if available
    if feedback:
        result = speech_synthesizer.speak_text_async(feedback).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesis failed for feedback.")
