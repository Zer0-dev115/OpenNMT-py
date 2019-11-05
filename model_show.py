import os
#import magic
import urllib.request
from app import app
from flask import Flask, request, redirect, render_template
import torch
import torchaudio
import librosa
from pydub import AudioSegment
import os
import uuid
from get_translation import main

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    uploaded_filename = uploaded_file.filename
    ext = os.path.splitext(uploaded_filename)[-1].lower()
    audio_id = "%4d"%uuid.uuid4().int
    allowed_ext=['.wav','.mp3','.flac']
    if ext in allowed_ext:
        filepath_audio = os.path.join(os.getcwd(),audio_id+ext)
        uploaded_filename = audio_id+ext
    else:
       return "file incompatible"
    print("file",filepath_audio)
    uploaded_file.save(filepath_audio)
    print("audio_saved")

    main(filepath_audio,uploaded_filename,ext)
    print("file translated")
    with open(os.getcwd()+"/pred.txt", 'r') as f:
        line = f.read()
        return line


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
