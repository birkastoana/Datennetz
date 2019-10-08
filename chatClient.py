#!/usr/bin/python3
import socket
import sys

TCP_IP = ''
TCP_PORT = 25
BUFFER_SIZE = 1024
UDP_IP = '127.0.0.255'
UDP_PORT = 3333

def sendDiscoverUDP():
    try:
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSock.connect((UDP_IP, UDP_PORT))
        udpSock.sendto(b'DISCOVER')
        res = udpSock.recv(BUFFER_SIZE)
        print(res)
    except:
        print("Es ist ein Fehler aufgetreten!")
        import traceback
        traceback.print_exc()

    finally:
        udpSock.close()


sendDiscoverUDP()