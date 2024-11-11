from transformers import pipeline
import sounddevice as sd
import wave
import tempfile

# Initialize Whisper with explicit language setting to avoid detection warning
whisper_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3-turbo",
    language="en",  # Force language to English
    device=0  # Use GPU for faster processing (set to -1 for CPU)
)


def record_audio(duration=5, fs=16000):
    """
    Record audio from the microphone for the specified duration and sample rate.
    :param duration: Duration of the recording in seconds
    :param fs: Sampling rate in Hz
    :return: Recorded audio as numpy array
    """
    print("Recording... Please speak clearly.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is done
    print("Recording complete.")
    return recording.flatten()


def transcribe_audio(audio_data):
    """
    Transcribe audio data using Whisper ASR model.
    :param audio_data: Audio data to transcribe
    :return: Transcribed text
    """
    print("Transcribing audio...")

    # Save the audio data to a temporary file for Whisper
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        with wave.open(tmp_file.name, 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(16000)  # Standard sampling rate for Whisper
            wf.writeframes(audio_data.tobytes())

        # Perform transcription with Whisper
        transcription = whisper_pipeline(tmp_file.name)

    print(f"Transcription: {transcription['text']}")
    return transcription['text']


# Run the transcription process
audio_data = record_audio(duration=5)  # Record for 5 seconds
transcription = transcribe_audio(audio_data)
