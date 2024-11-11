import time
from transformers import pipeline
from LensLab.voice_assistance import provide_voice_feedback, speech_synthesizer

# Whisper STT pipeline for voice command recognition
stt_pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo")

# Recognized commands
ACTIVATE_COMMAND = "navigation mode on"
DEACTIVATE_COMMAND = "navigation mode off"

# State for navigation mode
navigation_mode = False

def recognize_command(audio_input):
    """Convert audio input to text and return recognized command."""
    result = stt_pipe(audio_input)
    transcript = result['text'].lower()
    return transcript

def handle_voice_command(transcript):
    """Handle commands to toggle navigation mode."""
    global navigation_mode
    if ACTIVATE_COMMAND in transcript:
        if not navigation_mode:
            navigation_mode = True
            text = "Navigation mode is now on. I’ll assist you with object detection."
            speech_synthesizer.speak_text_async(text).get()
        else:
            text = "Navigation mode is already on."
            speech_synthesizer.speak_text_async(text).get()
    elif DEACTIVATE_COMMAND in transcript:
        if navigation_mode:
            navigation_mode = False
            text = "Alrighty, let me know if there's anything you need."
            speech_synthesizer.speak_text_async(text).get()
        else:
            text = "Navigation mode is already off."
            speech_synthesizer.speak_text_async(text).get()

    return navigation_mode
