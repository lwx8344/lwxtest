# coding=utf-8
#server服务器
import socket
address = ('0.0.0.0',9996)#本主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)


while 1:
    data,address=s.recvfrom(2048)
    if not data:
        break
    print("got data from",address)
    print(data.decode())
    if data.decode()=="happy":
        print("runrurnrun!")
s.close()