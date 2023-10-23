# Quickly import essential libraries
import queue
import sys
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from numpy.fft import fft, fftfreq
from scipy.signal import find_peaks, periodogram

guitar_notes = [82.41, 110, 146.83, 196, 246.94, 329.63]
total_peaks_required = [8, 7, 4, 3, 2, 2]

# Lets define audio variables
# We will use the default PC or Laptop mic to input the sound

device = 0 # id of the audio device by default
window = 5 # number of seconds to record
downsample = 1 # how much samples to drop
channels = [1] # a list of audio channels
interval = 0.1 # this is update interval in miliseconds for plot
freq_max = 1000 #maximum frequency to show on spectrum

# lets make a queue
q = queue.Queue()
# Please note that this sd.query_devices has an s in the end.
device_info =  sd.query_devices(device, 'input')
samplerate = device_info['default_samplerate']
length  = int(window*samplerate/downsample)

plotdata =  np.zeros((length,len(channels)))
freq = fftfreq(length, d=1/samplerate)
df = np.diff(freq)[0]
N = int(freq_max/df)

fig, axes = plt.subplots(1, 2, figsize=(10,4), width_ratios=[1,0.2])
ax = axes[0]
ax.set_title("PyShine")
lines = ax.plot(np.arange(length), np.arange(length), color = (0,1,0.29))
peak_lines = LineCollection([], color='r')
ax.add_collection(peak_lines)
ax.set_facecolor((0,0,0))
ax.set_yticks([0])
ax.yaxis.grid(True)
ax.semilogy()
ax.set_ylim(1e-12,1e-3)
ax.set_xlim(0,1000)
ax = axes[1]
#ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
ax.axhline(100)
line_tone = LineCollection([], color='r')
ax.add_collection(line_tone)
ax.set_ylim(96,104)

def audio_callback(indata,frames,time,status):
    q.put(indata[::downsample])
 
def check_freq(freq_peaks, note_frequency, total_peaks_required=4):
    total_peaks = np.sum(np.abs((freq_peaks/note_frequency - np.round(freq_peaks/note_frequency))/(freq_peaks/note_frequency))<0.02)
    if total_peaks>total_peaks_required:
        return True
    else:
        return False

def update_plot(frame):
    global plotdata
    while True:
        try: 
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis = 0)
        plotdata[-shift:,:] = data
    for column, line in enumerate(lines):
        freq, power_spectrum = periodogram(plotdata[:,column], samplerate)
        peaks = find_peaks(np.log10(power_spectrum[0:N]), height=-8, distance=80/df, prominence=2)[0]
        freq_peaks = freq[peaks]
        peak_lines.set_segments(np.array([[[f, 0], [f, 1e6]] for f in freq_peaks]))
        # Update right plot for specific guitar note automatically detected
        note = guitar_notes[np.argmax([check_freq(freq_peaks, note, peaks_required) for note, peaks_required in zip(guitar_notes, total_peaks_required)])]
        print(note)
        line_tone.set_segments(np.array([[[-100, f/note * 100], [100, f/note* 100]] for f in freq_peaks]))
        line.set_data(freq[:N], power_spectrum[:N])
    return peak_lines, *lines, line_tone

stream  = sd.InputStream(device = device, channels = max(channels), samplerate = samplerate, callback = audio_callback)

ani  = FuncAnimation(fig, update_plot, interval=interval, blit=True)
with stream:
    plt.show()