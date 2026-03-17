import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

model_name = "gemini-2.5-flash-native-audio-latest"
info = client.models.get(model=model_name)
print(f"=== {model_name} ===")
print(f"supported_actions: {info.supported_actions}")
print(f"endpoints: {info.endpoints}")
