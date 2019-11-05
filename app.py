from flask import Flask
import os 

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER