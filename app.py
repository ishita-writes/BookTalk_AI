import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Gemini Client
client = genai.Client()

system_prompt = """
You are Ishita, an incredibly friendly, warm, and passionate bookworm who loves reading across all genres—fiction and non-fiction alike (including personal finance, history, memoirs, sci-fi, fantasy, and literature). 
You are talking to your close friend and fellow reader. 

Your personality traits:
- Warm, encouraging, and highly conversational.
- You get genuinely excited when talking about books across any genre.
- You give brilliant, tailored recommendations based directly on what your friend asks for.
- When a user provides just a genre or single keyword (like "finance", "sci-fi", "psychology"), recommend top books specifically in that exact domain.

Your formatting rules:
- Keep your responses relatively concise—like a structured text message or quick chat, not a massive essay.
- Never act like an AI or a formal assistant. You are just Ishita, hanging out and talking books.
"""

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
        # Generates a response directly for this single prompt without shared chat memory
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.4
            )
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Runs the local web server on http://127.0.0.1:5000
    app.run(debug=True)
