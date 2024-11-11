# # Load the dataset
# from datasets import load_dataset
# from IPython.display import Audio
#
# ds = load_dataset("leafspark/openai-voices")
#
# # Iterate through the training dataset
# for i, sample in enumerate(ds['train']):
#     audio_data = sample['audio']
#     label = sample['label']
#
#     print(f"Sample {i + 1}:")
#     print(f"Audio: {audio_data}")
#     print(f"Label: {label}")
#     print("-------------------")
#
# # Example: Play the first audio sample
# audio_path = ds['train'][0]['audio']['path']
# Audio(audio_path)

# Use a pipeline as a high-level helper
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/llama-3.1-nemotron-70b-instruct",
  messages=[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is the farthest galaxy from Earth?"}],
  temperature=0.5,
  top_p=0.7,
  max_tokens=800,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")



