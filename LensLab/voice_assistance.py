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
FEEDBACK_COOLDOWN = 5


def provide_voice_feedback(detected_objects, class_names, image_width, image_height, mode):
    """
    Provide distinct voice feedback based on the mode (navigate or identify).
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
                    if object_name not in last_feedback_time or current_time - last_feedback_time[
                        object_name] > FEEDBACK_COOLDOWN:
                        response = responses.get(object_name, default_response.format(object_name=object_name))
                        feedback_parts.append(response)
                        last_feedback_time[object_name] = current_time

    if feedback_parts:
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
        speak_text("Say 'navigate' to start navigation, 'identify' to identify objects, or 'stop' to stop.")
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
    Speak text using Azure Speech SDK.
    """
    print(f"Speaking: {text}")
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis failed.")
