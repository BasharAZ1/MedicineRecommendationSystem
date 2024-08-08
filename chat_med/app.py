from flask import Flask, request, jsonify, session, render_template
from flask_session import Session
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)


app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

load_dotenv()

apikey = os.getenv('API_KEY')
openai.api_key = apikey



@app.route('/chat', methods=['POST'])
def chat():
    if 'conversation_context' not in session:
        session['conversation_context'] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    user_input = request.json.get('prompt')
    
    # Append the user message to the conversation context
    session['conversation_context'].append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=session['conversation_context'],
        max_tokens=250,
        temperature=0.5
    )

    assistant_response = response['choices'][0]['message']['content'].strip()


    session['conversation_context'].append({"role": "assistant", "content": assistant_response})


    session.modified = True

    return jsonify({"response": assistant_response})

@app.route('/reset', methods=['POST'])
def reset():
    session['conversation_context'] = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify({"message": "Conversation context reset."})

if __name__ == '__main__':
    app.run(debug=True)
