import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import speech_recognition as sr

# Plotting
plotdata =  np.array([])
fig,ax = plt.subplots(figsize=(8,4))
line, = ax.plot([], [], color = (0,1,0.29))

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize PyAudio
p = pyaudio.PyAudio()

# Parameters for audio capture
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = int(RATE / 0.3)  # 1 second per chunk

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

def update_plot(frame):
    data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
    line.set_data(np.arange(len(data)), data)
    return line,

def audio_callback(in_data, frame_count, time_info, status):
    # Get text
    audio_source = sr.AudioData(in_data, sample_rate=RATE, sample_width=2)
    try:
        text = recognizer.recognize_google(audio_source)
    except:
        text = ''
    # Get RMS
    in_data_numpy = np.frombuffer(in_data, dtype=np.int16)
    rms = np.std(in_data_numpy)
    print(f"Speech: {text}")
    if rms>3000:
        return (in_data, pyaudio.paAbort)
    else:
        return (in_data, pyaudio.paContinue)

FuncAnimation(fig, update_plot, interval=30, blit=True, frames=200)
plt.show()

stream.stop_stream()
stream.close()
p.terminate()