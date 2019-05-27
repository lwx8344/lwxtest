#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#server服务器 判断客户端发来的信号是否为happy，检测服务器摄像头是否检测到笑容。当二者均满足则运行。
from statistics import mode
import cv2
from keras.models import load_model
import numpy as np
from utils import preprocess_input
import schedule
import time
import threading
import socket
import RPi.GPIO as GPIO 
#以上为使用的库
Trig_Pin = 24  #超声波发送脚
Echo_Pin = 25  #超声波接收检测脚
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
GPIO.setup(16,GPIO.IN)
address = ('0.0.0.0',9999)#接收所有ip发过来的udp信息。
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)
#以上为网络连接部分

# parameters for loading data and images
detection_model_path = 'trained_models/facemodel/haarcascade_frontalface_default.xml'
#emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.33-0.65.hdf5'
emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.34-0.65.hdf5'
#以上为使用的算法模型
emotion_labels = {0:'angry',1:'disgust',2:'fear',3:'happy',
                4:'sad',5:'surprise',6:'neutral'}


global emotionnum
emotionnum = 0
#定义一个全局变量，统计一段时间的某种表情个数，并赋初值。

global flag
flag = 0
#定义一个全局变量，记录是否该让电机运转。

global run_state#状态值，0为检测笑脸，1为驱动电机前进，2为停止，3为返回
run_state=0  

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]#这里是输入张量的形状
emotion_window = []
frame_window = 10

def checkdist():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 * 100 / 2


def job1():
    global emotionnum
    emotionnum=0
    global flag
    flag=0
#表情标志位清0函数

def job2():
	pass
#一直检测是否两台椅子都检测到微笑

def job_task1():
	threading.Thread(target=job1).start()
#开一个新的线程执行清0任务

def runtimer():
	schedule.every(3).seconds.do(job_task1)
#每三秒进行一次定时给表情标志位清0任务




# starting video streaming
cv2.namedWindow('emotion_classifier') #弹出的界面左上角命名
#video_capture = cv2.VideoCapture('1.mp4')
video_capture = cv2.VideoCapture(0)
#这里可以切换读取的摄像头或者文件



runtimer()
#定时器函数
threading.Thread(target=job2).start()
while(1):
	while (run_state==0): 
		if emotionnum>4:
			print("检测到笑")
			flag=1
			run_state=1
			time.sleep(3)
	#检测到微笑则停止检测3秒，防止反复触发。

		schedule.run_pending()#定时器相关函数

		bgr_image = video_capture.read()[1]
		gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
		rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
		faces = face_detection.detectMultiScale(gray_image, 1.3, 5)
		for face_coordinates in faces:
			x1,y1,width,height = face_coordinates
			x1,y1,x2,y2 = x1,y1,x1+width,y1+height
			#x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
			gray_face = gray_image[y1:y2, x1:x2]
			try:
				gray_face = cv2.resize(gray_face, (emotion_target_size))
			except:
				continue
		   
			gray_face = preprocess_input(gray_face, True)
			gray_face = np.expand_dims(gray_face, 0)
			gray_face = np.expand_dims(gray_face, -1)
			emotion_prediction = emotion_classifier.predict(gray_face)
			#emotion_probability = np.max(emotion_prediction)
			emotion_label_arg = np.argmax(emotion_prediction)
			emotion_text = emotion_labels[emotion_label_arg]
			emotion_window.append(emotion_text)
			if len(emotion_window) > frame_window:
				#emotion_window.pop(0)
				if emotion_window.pop(0) == "happy":
					emotionnum=emotionnum+1
					print('当前记录的笑容个数：',emotionnum)
			try:
				emotion_text = mode(emotion_window)
			except:
				continue
			color = (0,0,255)
			cv2.rectangle(rgb_image,(x1,y1),(x2,y2),(0,0,255),2)
			cv2.putText(rgb_image,emotion_text,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
		bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
		cv2.imshow('emotion_classifier', bgr_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	while(run_state==1): 
		GPIO.output(21, GPIO.HIGH)
		print('正在前进,距离:', checkdist(), 'cm')
		if(checkdist()<20): #检测到足够近时
                    GPIO.output(21, GPIO.LOW)
                    print('已经停止')
                    run_state=2

	while (run_state==2): 
		print('正在检测是否有人离开椅子')
		if(GPIO.input(16)==0):
			run_state=3

	while(run_state==3): 
		print('正在后退，距离:', checkdist(), 'cm')
		GPIO.output(20, GPIO.HIGH)
		if(checkdist()>100): 
                    GPIO.output(20, GPIO.LOW)
                    print("停止，重新进行笑容识别")
                    run_state=0
		
