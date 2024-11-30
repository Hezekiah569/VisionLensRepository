from openai import OpenAI
import os
from dotenv import load_dotenv

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="nvidia/llama-3.1-nemotron-70b-instruct",
  messages=[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"How do we know that we are talking to an AI?"}],
  temperature=0.5,
  top_p=0.7,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

