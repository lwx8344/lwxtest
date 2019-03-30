# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)
while 1: 
	print('pin16电平值为：',GPIO.input(16))
