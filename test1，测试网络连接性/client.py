# coding=utf-8
#client�ͻ���
import socket
address = ('127.0.0.1',9996)#����IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(address)

while 1:
		str = input('Please input :')
		strInput=str.encode('utf-8')
		s.send(strInput)
		print("send success")