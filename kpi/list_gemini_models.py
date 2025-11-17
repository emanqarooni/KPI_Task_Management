import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env manually
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("🔑 Loaded API key:", "FOUND" if api_key else "NOT FOUND")

genai.configure(api_key=api_key)

print("\n🔍 Listing available models...\n")

models = genai.list_models()

for m in models:
    print(m.name)
