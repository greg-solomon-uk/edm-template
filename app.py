from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html",
        AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT"),
        AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY"),
        AZURE_OPENAI_MODEL=os.getenv("AZURE_OPENAI_MODEL")
    )
