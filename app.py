from flask import Flask, render_template, request, abort, json, jsonify
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import requests

load_dotenv()

app = Flask(__name__)

@app.after_request
def set_cookie_if_needed(response):
    response.set_cookie("ip_address", request.headers.get('X-Forwarded-For', request.remote_addr), path="/")
    return response

def list_yaml_files():
    yaml_files = []
    static_folder = os.path.join(app.root_path, 'static')
    for root, dirs, files in os.walk(static_folder):
        for file in files:
            if file.endswith('.yaml'):
                # Get path relative to the project root
                # relative_path = os.path.relpath(os.path.join(root, file), app.root_path)
                yaml_files.append(file)
    return sorted(yaml_files)

@app.route("/")
def index():
    yaml_files = list_yaml_files()
    return render_template("index.html", 
        YAML_FILES=yaml_files
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
    # return jsonify({"status": "saved"}), 200
    data = request.get_json()
    filename = data.get('filename')
    conversation_data = data.get('data')
    with open(f'cache/{filename}.json', 'w') as f:
        import json
        json.dump(conversation_data, f)
    return jsonify({"status": "saved"}), 200

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    conversation_history = data.get('conversation_history', [])
    instructions = data.get('instructions', '')
    
    if instructions:
        conversation_history.append({'role': 'system', 'content': instructions})

    try:
        response = requests.post(
            f"{os.getenv('AZURE_OPENAI_ENDPOINT')}/openai/deployments/{os.getenv('AZURE_OPENAI_MODEL')}/chat/completions?api-version=2025-01-01-preview",
            headers={
                'Content-Type': 'application/json',
                'api-key': os.getenv('AZURE_OPENAI_API_KEY')
            },
            json={
                'messages': conversation_history,
                'temperature': 0.7
            }
        )
        
        data = response.json()
        reply = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        conversation_history.append({'role': 'assistant', 'content': reply})
        
        return jsonify({
            'reply': reply,
            'conversation_history': conversation_history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500