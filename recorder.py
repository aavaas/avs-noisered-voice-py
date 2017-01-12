"""
avs modified into nonblocking recorder
PyAudio example: Record  audio and save to a WAVE file.
"""

import pyaudio
import wave
import noiseremove
from scipy.io import wavfile
import numpy as np


FRAMES_per_buffer = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
WAVE_OUTPUT_FILENAME = "recorded.wav"

p = pyaudio.PyAudio()
noiser = noiseremove.Noiseremover(RATE)

frames = []

def callback(in_data, frame_count, time_info, status):
            frames.append(in_data)
            return None, pyaudio.paContinue

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=FRAMES_per_buffer,
                 stream_callback=callback)

def startrecord():		
	print("* recording")
	global frames
	frames = []
	stream.start_stream()	


def stoprecord():
	print("* done recording")
	global frames
	stream.stop_stream()	


builtnoise = False
def removenoise():
	if builtnoise:
		rate, data = wavfile.read(WAVE_OUTPUT_FILENAME)
		data = data / (2. ** 15)  # convert quantised values into real value for 16bit audio    
		cleandata = noiser.removenoise(data)
		cleandata = cleandata * (2. ** 15)
		cleandata= np.array(cleandata, np.int16)
		wavfile.write('avassilenceremove.wav', rate, cleandata)

def buildnoiseprofile():
	global builtnoise
	ate, data = wavfile.read(WAVE_OUTPUT_FILENAME)
	data = data / (2. ** 15)  # convert quantised values into real value for 16bit audio
	noiser.buildnoiseprofile(data, nosecs=1)	
	builtnoise = True

def savefile():	
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

def closerecorder():
	stream.close()
	p.terminate()