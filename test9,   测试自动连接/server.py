
#!/usr/bin/env python 

# -*- coding:UTF-8 -*-

 

from socket import *

from time import ctime

 

HOST = '127.0.0.1'

PORT = 21567

BUFSIZE = 1024

 

ADDR = (HOST,PORT)

 

udpSerSock = socket(AF_INET, SOCK_DGRAM)

udpSerSock.bind(('',PORT))

print ('wating for message...')

while True:

    data, addr = udpSerSock.recvfrom(BUFSIZE)

    print('Server received from {}:{}'.format(addr, data.decode('utf-8')))
 

 

udpSerSock.close()
