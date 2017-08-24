# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 14:03:05 2017

@author: weiyu
"""

import pyaudio  
import wave  
import time
  
#define stream chunk   
chunk = 1024  
  

#open a wav format music  
f = wave.open(r"./voice/tts_jinzong.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = f.readframes(frame_count)
    return (data, pyaudio.paContinue)

#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True,
                 stream_callback=callback)  
#read data  
# data = f.readframes(chunk)  
print("debug")
#paly stream  
#stream.write(data)  
# while data != '':  
#     stream.write(data)  
#     data = f.readframes(chunk)  
#     print("play")
#     if not stream.is_active():
#     	break


# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

print("finish")
#stop stream  
stream.stop_stream()  
stream.close()  
  
#close PyAudio  
p.terminate()  