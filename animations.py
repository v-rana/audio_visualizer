import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

import scienceplots
import numpy as np
import pandas as pd
import sounddevice as sd
import pyaudio
import time
from audio_preprocessor import audio_preprocessing

#The default values
fs = 22050
seconds = 5
chunk = 4096

# Initialize PyAudio
p = pyaudio.PyAudio()
start_time = time.time()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=fs,
    input=True,
    frames_per_buffer=chunk
)

#Intializing the graph

fig, axis = plt.subplots()
ani_plot, = axis.plot([], [])

#Starting the recording
print("Recording...")

myrecording = np.array([], dtype=np.float16)


#preprocessor
pre_processor = audio_preprocessing(20)

#The function to update myrecording for the animation
def update_func(frame):
    global myrecording
    if time.time()-start_time < seconds:
        data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        data = abs(data)
        data = pre_processor.condense(data)
        myrecording = np.concatenate((myrecording, data))
        axis.set_xlim(0, len(myrecording))
        axis.set_ylim(0,1)
        ani_plot.set_data(np.arange(len(myrecording)),myrecording)
        return ani_plot,
    else:
        return ani_plot,

animation = FuncAnimation(fig, update_func, interval=25,blit=True)

try:
    plt.show()
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

print("Finished recording!")
	


