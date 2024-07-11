import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import time
from audio_preprocessor import audio_preprocessing


#To be implemented
# if 'key' not in st.session_state:
#     st.session_state['key'] = 'Not recording'
# st.write(st.session_state.key)


# The default values
fs = 22050
chunk = 4096

#initialize all streamlit inputs
st.title('Audio Visualization')
rec_time = st.sidebar.slider(
    'Select a range of values',
    1, 60, (20)
)
Number_of_points = st.sidebar.number_input('Number of points',
                                           min_value=5,max_value=chunk,
                                           value=20,step=10)
seconds = rec_time 

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

# Initialize the graph
fig, axis = plt.subplots()
line, = axis.plot([], [])

# Preprocessor
pre_processor = audio_preprocessing(20)

# Function to update data for the plot
def update_plot():
    myrecording = np.array([], dtype=np.float16)
    plot_placeholder = st.empty()
    while time.time() - start_time < seconds:

        data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        data = abs(data)
        data = pre_processor.condense(data)
        myrecording = np.concatenate((myrecording, data))

        axis.clear()
        axis.plot(myrecording)
        plot_placeholder.pyplot(fig)
        time.sleep(0.05)
    else:
        plot_placeholder.pyplot(fig)
        

# Button to start recording
start_button = st.button('Start Plotting')

if start_button :
    update_plot()


# Close the stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
