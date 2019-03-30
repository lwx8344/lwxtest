#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from statistics import mode
import cv2
from keras.models import load_model
import numpy as np
from utils import preprocess_input
import schedule
import time
import threading
import socket
#以上为使用的库



# parameters for loading data and images
detection_model_path = 'trained_models/facemodel/haarcascade_frontalface_default.xml'
#emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.33-0.65.hdf5'
emotion_model_path = 'trained_models/float_models/fer2013_mini_XCEPTION.34-0.65.hdf5'

#以上为使用的算法模型
emotion_labels = {0:'angry',1:'disgust',2:'fear',3:'happy',
                4:'sad',5:'surprise',6:'neutral'}





face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]#这里是输入张量的形状
emotion_window = []
frame_window = 10
#这个值表示连续测到多少次才显示表情，值越高，显示延迟越大，值过低则显示表情的文字变化过快。

# starting video streaming
cv2.namedWindow('Emotion_Classifier') #弹出的界面左上角命名
#video_capture = cv2.VideoCapture('1.mp4')
video_capture = cv2.VideoCapture(0)
#这里可以切换读取的摄像头或者文件
while True: 
    bgr_image = video_capture.read()[1]
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    faces = face_detection.detectMultiScale(gray_image, 1.3, 5)
#调用opencv自带的人脸识别器,此时的faces里面表明着脸部的位置和大小

    for face_coordinates in faces:
        x1,y1,width,height = face_coordinates
        x1,y1,x2,y2 = x1,y1,x1+width,y1+height
        gray_face = gray_image[y1:y2, x1:x2]
#把人脸部的图片单独抠出来
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
#缩放到合适的尺寸
        except:
            continue
        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
#图像转变为数组来计算

        emotion_prediction = emotion_classifier.predict(gray_face)#预测模式
        emotion_label_arg = np.argmax(emotion_prediction)

#预测出结果
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)
#结果转化成英文
        if len(emotion_window) > frame_window:
            emotion_window.pop(0)

        try:
            emotion_text = mode(emotion_window)
        except:
            continue
        color = (0,0,255)
        cv2.rectangle(rgb_image,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.putText(rgb_image,emotion_text,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
#把要显示的文字放在视频中
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('Emotion_Classifier', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
