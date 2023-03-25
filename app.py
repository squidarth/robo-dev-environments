from flask import Flask, send_from_directory
from tasks import create_development_environment
app = Flask(__name__, static_url_path='', static_folder='frontend/build')


@app.route("/")
def index():
    return send_from_directory(app.static_folder,'index.html')

@app.route("/create-dev-environment")
def create_dev_environment():


    pass