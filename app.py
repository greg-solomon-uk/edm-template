from flask import Flask, render_template, request, abort, json, jsonify
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import re
import requests
import litellm

load_dotenv()

app = Flask(__name__)

def list_yaml_files():
    yaml_files = []
    static_folder = os.path.join(app.root_path, 'static')
    for root, dirs, files in os.walk(static_folder):
        for file in files:
            if file.endswith('.yaml'):
                yaml_files.append(file)
    return sorted(yaml_files)

@app.route("/")
def index():
    yaml_files = list_yaml_files()
    return render_template("index.html", 
        YAML_FILES=yaml_files
    )

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    conversation_history = data.get('conversation_history', [])
    new_path = []
    for item in conversation_history:
        if item.get('role') == 'user':
            item = item.get('content')
            item = re.sub(r'[^\w\d]+', '_', item)   # Replace non-alphanumeric characters with underscores
            new_path.append(item)
    os.makedirs(os.path.join('cache', *new_path[:-1]), exist_ok=True)
    cache_path = os.path.join('cache', *new_path[:-1], new_path[-1] + '.json')
    instructions = data.get('instructions', '')
    
    # Try to load from cache first
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                return jsonify({'conversation_history': json.load(f)})
        except Exception as e:
            print(f"Cache read error: {str(e)}")
    
    # If no cache or cache read failed, generate new response
    if instructions:
        conversation_history.append({'role': 'system', 'content': instructions})

    try:
        litellm.api_base = "https://openai.generative.engine.capgemini.com/v1"

        response = litellm.completion(
            model = "openai/openai.gpt-4o",
            messages = conversation_history
        )

        data = response.json()
        reply = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        conversation_history.append({'role': 'assistant', 'content': reply})
        
        # Save to cache
        try:
            os.makedirs('cache', exist_ok=True)
            with open(cache_path, 'w') as f:
                json.dump(conversation_history, f)
        except Exception as e:
            print(f"Cache write error: {str(e)}")

        return jsonify({'conversation_history': conversation_history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500