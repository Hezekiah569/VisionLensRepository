import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

# Speech service subscription key and region
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-JaneNeural"

# SSML text with speaking style
ssml_text = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
    <voice name='en-US-JaneNeural'>
        <mstts:express-as style='cheerful'>
            Hi, this is Katniss speaking in a cheerful tone!
        </mstts:express-as>
    </voice>
</speak>
"""

# Initialize speech synthesizer
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize speech using SSML
result = speech_synthesizer.speak_ssml_async(ssml_text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized with style successfully!")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
