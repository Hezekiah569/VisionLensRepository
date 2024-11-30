# import azure.cognitiveservices.speech as speechsdk
# from openai import OpenAI
#
# # Azure Speech API Configuration
# speech_key = "9Wkhj4y02ULHOlISgoilMdkcOL0XFoXV8D9XdJhTuQ9vuVUTlS4KJQQJ99AKAC3pKaRXJ3w3AAAYACOG5uOL"
# service_region = "eastasia"
#
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# speech_config.speech_synthesis_voice_name = "en-US-JaneNeural"
#
# # OpenAI LLM API Configuration
# llm_client = OpenAI(
#     base_url="https://visionassistai.openai.azure.com/",
#     api_key="3jGgAxD7pRZr0asu1G983hDPPjbvsslwF3FpBCnNRu81y1XaGGTPJQQJ99AKACi0881XJ3w3AAABACOGNqPY"
# )
#
#
# # Function to get the user question
# def get_user_input():
#     return input("Enter your question: ")
#
#
# # Function to call the LLM API for answering the question
# def get_llm_response(question):
#     max_tokens = 200  # Adjust based on your use case
#     completion = llm_client.chat.completions.create(
#         model="gpt-35-turbo",  # Use the appropriate model for your LLM
#         messages=[{"role": "system", "content": "You are a helpful assistant."},
#                   {"role": "user", "content": question}],
#         temperature=0.7,
#         max_tokens=max_tokens
#     )
#
#     response = completion.choices[0].message.content
#
#     # Add a safety check to truncate responses that exceed character limits
#     max_response_length = 750  # Adjust as needed
#     if len(response) > max_response_length:
#         response = response[:max_response_length] + "... (response truncated)"
#
#     return response
#
#
# # Function to synthesize and speak text using Azure Speech
# def speak_text(response_text):
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
#     result = speech_synthesizer.speak_text_async(response_text).get()
#
#     # Check the result for errors
#     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#         print("Speech synthesized successfully!")
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = result.cancellation_details
#         print(f"Speech synthesis canceled: {cancellation_details.reason}")
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print(f"Error details: {cancellation_details.error_details}")
#
#
# # Main Function
# def main():
#     print("Welcome to the LLM-Azure Speech Test!")
#     user_question = get_user_input()
#
#     print("Querying the LLM...")
#     llm_response = get_llm_response(user_question)
#     print(f"LLM Response: {llm_response}")
#
#     print("Synthesizing speech for the response...")
#     speak_text(llm_response)
#
#
# if __name__ == "__main__":
#     main()


import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

# Azure Speech API Configuration
speech_key = "9Wkhj4y02ULHOlISgoilMdkcOL0XFoXV8D9XdJhTuQ9vuVUTlS4KJQQJ99AKAC3pKaRXJ3w3AAAYACOG5uOL"
service_region = "eastasia"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-JaneNeural"

# OpenAI LLM API Configuration
llm_client = AzureOpenAI(
    base_url="https://visionassistai.openai.azure.com/openai/deployments/testgpt35turbo16k/chat/completions?api-version=2024-08-01-preview",
    api_key="3jGgAxD7pRZr0asu1G983hDPPjbvsslwF3FpBCnNRu81y1XaGGTPJQQJ99AKACi0881XJ3w3AAABACOGNqPY",
    api_version="2024-08-01-preview"
)

# Function to get the user question
def get_user_input():
    return input("Enter your question: ")

# Function to call the LLM API for answering the question
def get_llm_response(question):
    max_tokens = 200  # Adjust based on your use case
    completion = llm_client.chat.completions.create(
        model="testgpt35turbo16k",  # Use the appropriate model for your LLM
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": question}],
        temperature=0.7,
        max_tokens=max_tokens
    )

    response = completion.choices[0].message.content

    # Add a safety check to truncate responses that exceed character limits
    max_response_length = 750  # Adjust as needed
    if len(response) > max_response_length:
        response = response[:max_response_length] + "... (response truncated)"

    return response

# Function to synthesize and speak text using Azure Speech
def speak_text(response_text):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(response_text).get()

    # Check the result for errors
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# Main Function
def main():
    print("Welcome to the LLM-Azure Speech Test!")
    user_question = get_user_input()

    print("Querying the LLM...")
    llm_response = get_llm_response(user_question)
    print(f"LLM Response: {llm_response}")

    print("Synthesizing speech for the response...")
    speak_text(llm_response)

if __name__ == "__main__":
    main()
