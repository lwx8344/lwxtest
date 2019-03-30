#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#server服务器 判断客户端发来的信号是否为happy，检测服务器摄像头是否检测到笑容。当二者均满足则运行。
from statistics import mode
import schedule
import time
import threading
import socket
import RPi.GPIO as GPIO #以上为使用的库
Trig_Pin = 23  #超声波发送脚
Echo_Pin = 24  #超声波接收检测脚
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,10000)
pwm.start(97)
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
GPIO.setup(16,GPIO.IN)

address = ('0.0.0.0',9999)#接收所有ip发过来的udp信息。
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)#以上为网络连接部分
#video_capture = cv2.VideoCap
global emotionnum#定义一个全局变量，统计一段时间的某种表情个数，并赋初值。
emotionnum = 0
global flag#定义一个全局变量，记录是否该让电机运转。
flag = 0
global run_state#状态值，0为检测笑脸，1为驱动电机前进，2为停止，3为返回
run_state=1  

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



while (run_state==1): 
    GPIO.output(20, GPIO.HIGH)
    print('距离:', checkdist(), 'cm')
    if(checkdist()<30): 
        GPIO.output(20, GPIO.LOW)
        run_state=2

while (run_state==2): 
    print('距离:', checkdist(), 'cm')
    if(GPIO.input(16)==1):
        run_state=3

while (run_state==3): 
    print('距离:', checkdist(), 'cm')
    GPIO.output(21, GPIO.high)
    if(checkdist()>100): 
            GPIO.output(21, GPIO.LOW)
            run_state=4
            print("测试结束")


