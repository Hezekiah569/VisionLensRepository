import pyttsx3

engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# List all voices
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name}, ID: {voice.id}")
