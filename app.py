from flask import Flask, render_template, request, abort
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

load_dotenv()

app = Flask(__name__)

SECRET_NAME = "user-token"
KEY_VAULT_NAME = os.getenv("AZURE_KEY_VAULT_NAME", "edm-coach-keyvault")

# Initialize Azure Key Vault client
vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=vault_url, credential=credential)
EXPECTED_VALUE = secret_client.get_secret(SECRET_NAME).value

@app.before_request
def check_cookie():
    if request.cookies.get(SECRET_NAME) is None:
        request.user_token = "UNSET"
    else:
        request.user_token = request.cookies.get(SECRET_NAME)

@app.after_request
def set_cookie_if_needed(response):
    response.set_cookie("ip_address", request.headers.get('X-Forwarded-For', request.remote_addr), path="/")
    if getattr(request, 'user_token', None) == "UNSET":
        response.set_cookie(SECRET_NAME, "UNSET", path="/")
    if getattr(request, 'user_token', None) != EXPECTED_VALUE:
        abort(403)  # Forbidden
    return response

@app.route("/")
def index():
    return render_template("chat.html",
        AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT"),
        AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY"),
        AZURE_OPENAI_MODEL=os.getenv("AZURE_OPENAI_MODEL")
    )
