import subprocess
import librosa
import webrtcvad
import numpy as np
import soundfile as sf
import os
from dotenv import load_dotenv
load_dotenv()

def convert_to_wav(input_path, output_path="temp.wav", sr=16000):
    output_path=os.getenv("in_base_path")+output_path
    ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
    command = [ffmpeg_path, "-y", "-i", input_path, "-ac", "1", "-ar", str(sr), output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return output_path

def load_audio(file_path, sr=16000):
    y, sr = librosa.load(file_path, sr=sr)
    return y, sr

def frame_generator(signal, frame_duration_ms, sample_rate):
    frame_size = int(sample_rate * frame_duration_ms / 1000)
    offset = 0
    while offset + frame_size < len(signal):
        yield signal[offset:offset + frame_size]
        offset += frame_size

def is_speech_frame(frame, vad, sample_rate):
    pcm_data = (frame * 32768).astype(np.int16).tobytes()
    return vad.is_speech(pcm_data, sample_rate)

def separate_speech_nonspeech(audio_path, speech_output="speech.wav", nonspeech_output="nonspeech.wav"):
    wav_path = convert_to_wav(audio_path)
    folder=audio_path.split("/")[-1].split(".")[0]
    base_path=os.getenv("base_path")+folder+"/"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    speech_output=base_path+speech_output
    nonspeech_output=base_path+nonspeech_output
    signal, sr = load_audio(wav_path)
    vad = webrtcvad.Vad(2)
    frame_duration_ms = 30

    speech, nonspeech = [], []

    for frame in frame_generator(signal, frame_duration_ms, sr):
        if is_speech_frame(frame, vad, sr):
            speech.extend(frame)
        else:
            nonspeech.extend(frame)

    if speech:
        speech = np.array(speech)
        speech /= np.max(np.abs(speech))
        sf.write(speech_output, speech, sr)

    if nonspeech:
        nonspeech = np.array(nonspeech)
        nonspeech /= np.max(np.abs(nonspeech))
        sf.write(nonspeech_output, nonspeech, sr)

    print("✅ Done. Files saved:")
    print(f" - Speech: {speech_output}")
    print(f" - Non-Speech: {nonspeech_output}")

# Usage
input_path=os.getenv("in_base_path")+"traffic_mix.m4a"
separate_speech_nonspeech(input_path)
