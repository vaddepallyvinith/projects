import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# Dynamically pick an available working model
model_name = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        model_name = m.name
        break

if not model_name:
    raise Exception("No compatible Gemini model found")

print(f"Using model: {model_name}")
model = genai.GenerativeModel(model_name)

# 1. Ask the user for a PDF file
pdf_path = input("Enter the path to your PDF file: ").strip()

if not os.path.exists(pdf_path):
    print("File not found. Please make sure the path is correct.")
    exit(1)

print(" Uploading and processing PDF...")
try:
    # 2. Upload the file to Gemini natively 
    uploaded_file = genai.upload_file(path=pdf_path)
    print("PDF successfully uploaded!")
except Exception as e:
    print(f"Failed to upload PDF: {e}")
    exit(1)

# 3. Start a chat with the PDF passed in the initial history
chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [uploaded_file, "Please read this document. I will ask questions about it."]
        },
        {
            "role": "model",
            "parts": ["I have read the document. What would you like to know?"]
        }
    ]
)

print("\n Gemini PDF Chatbot started! (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        # It's good practice to delete the file from Google's servers when done
        genai.delete_file(uploaded_file.name)
        break

    try:
        response = chat.send_message(user_input)
        print("🤖 Bot:", response.text, "\n")

    except Exception as e:
        print("Error:", e)
