from flask import Flask
from flask_cors import CORS
import os 

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)
CORS(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
