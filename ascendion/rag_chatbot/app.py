import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# Global state to hold chat session (for simplicity)
active_chat = None
uploaded_file = None

model_name = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        model_name = m.name
        break

if not model_name:
    raise Exception("No compatible Gemini model found")

model = genai.GenerativeModel(model_name)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    global active_chat, uploaded_file
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save temporarily to upload to gemini
    temp_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(temp_path)
    
    try:
        # Delete old file if exists
        if uploaded_file:
            try:
                genai.delete_file(uploaded_file.name)
            except Exception:
                pass
                
        uploaded_file = genai.upload_file(path=temp_path)
        
        # Initialize new chat
        active_chat = model.start_chat(
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
        return jsonify({"message": "File uploaded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route("/chat", methods=["POST"])
def chat():
    global active_chat
    if not active_chat:
        return jsonify({"error": "Please upload a PDF first."}), 400
        
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required."}), 400
        
    try:
        response = active_chat.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
