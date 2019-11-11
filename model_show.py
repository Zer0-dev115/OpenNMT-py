import os
#import magic
import urllib.request
from app import app
from flask import Flask, request, redirect, render_template
from flask_cors import CORS
import torch
import torchaudio
import librosa
from pydub import AudioSegment
import os
import uuid
import get_translation

CORS(app)
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
    uploaded_file.save(filepath_audio)
    print("audio_saved")
    filename = get_translation.change_extension(filepath_audio,uploaded_filename,ext)
    upload_filename = audio_id+".wav"
    outfile = get_translation.sampling(filename,upload_filename)
    print("outfile",outfile)
    line = get_translation.segmentation(outfile)
    print("file translated")

    os.remove(os.getcwd()+"/transmultiple.txt")
    os.remove(filename)
    return line


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
