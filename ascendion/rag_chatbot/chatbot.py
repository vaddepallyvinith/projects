import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# ✅ Auto-pick a working model
model_name = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        model_name = m.name
        break

if not model_name:
    raise Exception("❌ No compatible Gemini model found")

print("✅ Using model:", model_name)

model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

print("🤖 Gemini Chatbot started! (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("👋 Goodbye!")
        break

    try:
        response = chat.send_message(user_input)
        print("🤖 Bot:", response.text, "\n")

    except Exception as e:
        print("❌ Error:", e)