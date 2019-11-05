import torch
import torchaudio
import librosa
from pydub import AudioSegment
import os


def change_extension(filename,uploaded_file,ext):
    if ext == ".mp3":
        song = AudioSegment.from_file(uploaded_file, format="mp3")
        sourcewav=os.path.splitext(uploaded_file)[0]
        uploaded_file = '%s.wav'%sourcewav
        song.export(os.getcwd()+uploaded_file,format = "wav")
        filename = os.getcwd()+uploaded_file
    elif ext == ".flac":
        song = AudioSegment.from_file(uploaded_file, format="flac")
        sourcewav=os.path.splitext(uploaded_file)[0]
        uploaded_file = '%s.wav'%sourcewav
        song.export(os.getcwd()+uploaded_file,format = "wav")
        filename = os.getcwd()+uploaded_file
    elif ext == ".wav":
        filename = filename
    else:
        print("file is not in acceptable format(wav,flac,mp3)")
    return filename, uploaded_file

def sampling(filename,uploaded_file):
    y, sr = torchaudio.load(filename)
    global outfile
    if sr == 16000:
        outfile = filename
        print("sample rate correct.")
    else:
        outfile = os.path.join(os.getcwd()+"/translation_data/", "%s" % uploaded_file)
        os.system(
            'sox {0} -b 16 -e signed-integer -c 1 -r 16k -t wav {1}'.format(filename, outfile))
        print("sample rate changed successfully.")
    return outfile

def segmentation(filename):
    audio = AudioSegment.from_wav(outfile)
    n = len(audio)
    if n <= 20000:
        with open(os.getcwd()+"/trans.txt", 'w') as f:
            f.write(outfile)
            f.close()
            print("file created1")
    else:
        counter = 1
        interval = 10 * 1000
        overlap = 0.5 * 1000
        start = 0
        end = 0
        flag = 0
        for i in range(0, 2 * n, interval):
            if i == 0:
                start = 0
                end = interval
            else:
                start = end - overlap
                end = start + interval
            if end >= n:
                end = n
                flag = 1
            chunk = audio[start:end]
            filename_chunk = 'audio_part'+str(counter)+'.wav'
            chunk.export(filename, format="wav")
            counter = counter + 1

            with open(os.getcwd()+"/trans.txt", 'a') as f:
                f.write(filename_chunk)
                f.close()
                print("file created2")
    
    os.system('python3 translate.py -data_type audio -model models/demo-model-libri-sgd_step_90000.pt -src_dir translation_data -src trans.txt -output pred.txt -verbose -window_size 0.025 -image_channel_size 1 -beam_size 10 ')
    
    print("speech translation done!!")
    os.remove(os.getcwd()+"/trans.txt")
    os.remove(filename)
    

def main(filename,uploaded_file,ext):
    change_extension(filename,uploaded_file,ext)
    sampling(filename,uploaded_file)
    segmentation(filename)
