from flask import Flask, render_template, request, abort, json, jsonify
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

load_dotenv()

app = Flask(__name__)

@app.after_request
def set_cookie_if_needed(response):
    response.set_cookie("ip_address", request.headers.get('X-Forwarded-For', request.remote_addr), path="/")
    return response

@app.route("/")
def index():
    return render_template("index.html",
        AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT"),
        AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY"),
        AZURE_OPENAI_MODEL=os.getenv("AZURE_OPENAI_MODEL")
    )

@app.route("/chat")
def chat():
    return render_template("chat.html",
        AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT"),
        AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY"),
        AZURE_OPENAI_MODEL=os.getenv("AZURE_OPENAI_MODEL")
    )

@app.route('/load-conversation', methods=['GET'])
def load_conversation():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    file_path = f'cache/{filename}.json'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                conversation = json.load(f)
            return jsonify({'data': conversation}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to load conversation', 'details': str(e)}), 500
    else:
        return jsonify({'data': None}), 200

@app.route('/save-conversation', methods=['POST'])
def save_conversation():
    data = request.get_json()
    filename = data.get('filename')
    conversation_data = data.get('data')
    # Your logic here to save the conversation (e.g., to a file or database)
    # For example, saving to a file:
    with open(f'cache/{filename}.json', 'w') as f:
        import json
        json.dump(conversation_data, f)
    return jsonify({"status": "saved"}), 200