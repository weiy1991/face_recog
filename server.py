#coding=utf-8
__author__ = 'jason'
'''
server端
长连接，短连接，心跳
'''
import socket
import simplejson 
import pyaudio  
import wave  
import time

###audio####
audio_melody = "./voice/tts_yinmin.wav"  #id 1
audio_jason = "./voice/tts_jason.wav"   #id  3
audio_michael = "./voice/tts_michael.wav"  #id  5
audio_tony = "./voice/tts_jinzong.wav"   #id  4

#####dic#####
audio_file = { "1" : audio_melody, 
		"3" : audio_jason, 
		"5" : audio_michael, 
		"4" : audio_tony, 
		}

audio_has_read = {
	"1": 0,
	"3": 0,
	"5": 0,
	"4": 0,
} 

#audio_sunny = "./voice/tts_jinzong.wav" 

count = 0

#define stream chunk   
def playaudio(id):
	#define stream chunk   
	chunk = 1024  
	
	audio_file_now = ""
	if str(id) in audio_file :
		if audio_has_read[str(id)] == 0 :
			audio_file_now = audio_file[str(id)]
			audio_has_read[str(id)] = 1
		else:
			return 0

	else:
		return 0


	#open a wav format music  
	f = wave.open( audio_file_now, "rb")  
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

###########
#playaudio(1)
print("begin to server")

BUF_SIZE = 1024
host = 'localhost'
port = 8083
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1) #接收的连接数
client, address = server.accept() #因为设置了接收连接数为1，所以不需要放在循环中接收



while True: #循环收发数据包，长连接
    data_buff = client.recv(BUF_SIZE)


    print("decoding type:",type(data_buff.decode())) #python3 要使用decode
    print("decoding:",data_buff.decode()) #python3 要使用decode
    print('buf type', type(data_buff))  

    count+=1

    if count>10:
    	audio_has_read["1"] = 0
    	audio_has_read["3"] = 0
    	audio_has_read["5"] = 0
    	audio_has_read["4"] = 0
    	count = 0


    if data_buff.decode().count("name") > 1:
    	continue


    dic = simplejson.loads(data_buff)  
    print('after loads', type(dic))  
    print(dic)  
    #time.sleep(1)
    if dic["ID"] != -1:
    	playaudio(dic["ID"])


    ##################
    #print(data.decode()) #python3 要使用decode

client.close() #连接不断开，长连接