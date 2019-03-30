# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,10000)
pwm.start(0)
i=1
try:
	while i: 
		pwm.ChangeDutyCycle(i)
		i=i+1
		time.sleep(0.05)
		print('速度为: %d '% i)
		if i==97:
			while i>2:
				print('速度为：%d'%i)
				pwm.ChangeDutyCycle(i)
				i=i-1
				time.sleep(0.05)
finally:
	print("clean up all GPIO..." )
