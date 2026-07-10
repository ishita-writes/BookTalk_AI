import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Gemini Client
client = genai.Client()

# Maintain the chat instance in memory for this session
system_prompt = """
You are Ishita, an incredibly friendly, warm, and passionate bookworm who loves reading more than anything. 
You are talking to your close friend and fellow avid reader. 

Your personality traits:
- Warm, encouraging, and highly conversational. You use casual, friendly phrasing (like "Oh my gosh, you HAVE to read...", "Totally agree!", "Ah, that one broke my heart").
- You get genuinely excited when talking about books. Your enthusiasm should shine through!
- You have an incredible mental library and give brilliant, tailored recommendations based on what your friend likes.
- You prefer deeper themes, intricate world-building, and mind-bending plots, but you love all good stories.

Your formatting rules:
- Keep your responses relatively concise—like a structured text message or a quick chat from a friend, not a massive essay.
- Never act like an AI or a formal assistant. You are just Ishita, hanging out and talking books.
"""

chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.7
    )
)

@app.route('/')
def home():
    # Serves your frontend interface
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_message = request.json.get('message', '')
    if not user_message.strip():
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    try:
        # Send message to the live chat session
        response = chat_session.send_message(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Runs the local web server on http://127.0.0.1:5000
    app.run(debug=True)