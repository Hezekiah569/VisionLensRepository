from LensLab.samantha_config import (
    IDENTIFY_MODE_OBJECTS,
    NAVIGATE_MODE_OBJECTS,
    IDENTIFY_MODE_RESPONSES,
    NAVIGATE_MODE_RESPONSES,
    DEFAULT_IDENTIFY_RESPONSE,
    DEFAULT_NAVIGATE_RESPONSE
)

import time
import azure.cognitiveservices.speech as speechsdk
import speech_recognition as sr
from dotenv import load_dotenv
import os

load_dotenv()

# Azure Speech SDK configuration
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

last_feedback_time = {}
FEEDBACK_COOLDOWN = 8.5

def get_object_direction(bbox, image_width):
    """
    Determine the direction of an object based on its bounding box.
    """
    x, y, width, height = bbox
    center_x = x + (width / 2)

    if center_x < image_width * 0.33:
        return "left"
    elif center_x > image_width * 0.66:
        return "right"
    return "front"

def provide_voice_feedback(detected_objects, class_names, image_width, image_height, mode):
    """
    Provide distinct voice feedback based on the mode (navigate or identify), with cooldown logic.
    """
    global last_feedback_time
    current_time = time.time()

    valid_objects = (
        NAVIGATE_MODE_OBJECTS if mode == "navigate" else IDENTIFY_MODE_OBJECTS
    )
    responses = (
        NAVIGATE_MODE_RESPONSES if mode == "navigate" else IDENTIFY_MODE_RESPONSES
    )
    default_response = (
        DEFAULT_NAVIGATE_RESPONSE if mode == "navigate" else DEFAULT_IDENTIFY_RESPONSE
    )

    feedback_parts = []

    for obj in detected_objects:
        if 'class' in obj and 'bbox' in obj:
            index = obj['class']
            if 0 <= index < len(class_names):
                object_name = class_names[index]
                if object_name in valid_objects:
                    # Check if enough time has passed since the last feedback for this object
                    last_time = last_feedback_time.get(object_name, 0)
                    if current_time - last_time > FEEDBACK_COOLDOWN:
                        direction = get_object_direction(obj['bbox'], image_width)
                        response_template = responses.get(object_name, {})
                        response = response_template.get(direction, default_response)
                        response = response.format(object_name=object_name, direction=direction)
                        feedback_parts.append(response)

                        # Update the last feedback time for this object
                        last_feedback_time[object_name] = current_time

    if feedback_parts:
        # Combine all responses and speak at once
        speak_text(" ".join(feedback_parts))

def handle_command(input_text, is_navigating, is_identifying):
    """
    Handle voice commands and set modes accordingly.
    """
    if input_text.lower() == "navigate":
        speak_text("Starting navigation mode.")
        return True, False
    elif input_text.lower() == "identify":
        speak_text("Starting identify mode.")
        return False, True
    elif input_text.lower() == "stop":
        speak_text("Stopping all modes.")
        return False, False
    elif input_text.lower() == "tutorial":
        speak_text(
        "Welcome to the navigation assistant tutorial. Here’s a quick guide on how to interact with me:"
        " Say 'navigate' to enter navigation mode. In this mode, I will guide you through your surroundings "
        "and describe nearby objects, obstacles, and directions."
        " Say 'identify' to switch to identification mode, where I will help you recognize specific objects, "
        "such as coins, furniture, or devices, and tell you their positions relative to you."
        " Say 'stop' to exit the current mode or end our interaction."
        " You can also say 'help' at any time to hear these instructions again."
        " Now, go ahead and say one of the commands: 'navigate', 'identify', or 'stop'.")
    return is_navigating, is_identifying

def recognize_command(recognizer, microphone):
    """
    Listen and recognize user commands.
    """
    with microphone as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        input_text = recognizer.recognize_google(audio, language="en-US").strip()
        print(f"Recognized command: {input_text}")
        return input_text
    except sr.UnknownValueError:
        print("Command not recognized.")
    except sr.RequestError as e:
        speak_text("There was an error with the speech recognition service.")
        print(f"Speech recognition service error: {e}")
    return None

def speak_text(text):
    """
    Speak text using Azure Speech SDK with slower speech rate.
    """
    print(f"Speaking: {text}")
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
        <voice name='{speech_config.speech_synthesis_voice_name}'>
            <mstts:express-as style='default'>
                <prosody rate='-15%'>
                    {text}
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    result = speech_synthesizer.speak_ssml_async(ssml_text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis failed.")
