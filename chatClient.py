#!/usr/bin/python3
import socket
import re
import sys
import logging
import threading
import time
from signal import signal, SIGINT

TCP_IP = ''
TCP_PORT = 25
BUFFER_SIZE = 1024
UDP_IP = '255.255.255.255'
UDP_PORT = 3333

def handler(signum, frame):
    print("ctr+c detected! exiting gracefully!")
    exit(0)

def sendDiscoverUDP():
    try:
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # udpSock.connect((UDP_IP, UDP_PORT))
        udpSock.settimeout(5)
        udpSock.sendto(b'DISCOVER', ("<broadcast>", 3333))
        response = udpSock.recv(BUFFER_SIZE)
        print("Response: %s" %response)
        response = re.match(b"ADDR (\d+.\d+.\d+.\d+):(\d+)", response)
        TCP_IP = response[1]
        TCP_PORT = response[2]
        return response
    except:
        return None
    finally:
        udpSock.close()


def chatListener(sock):
    while True:
        try:
            recvMsg = sock.recv(BUFFER_SIZE)
            print(recvMsg)
        except:
            break

def chatWriter(sock):
    sock.send(b"CONNECT kriskros\r\n")
    while True:
        try:
            sendMsg = input("promt")
            sock.send(sendMsg.encode())
        except:
            sock.send(b"DISCONNECT kriskros\r\n")

def socketThread(function):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))
        function(sock)
    except:
        print("Error!")
        import traceback
        traceback.print_exc()
    finally:
        sock.close()



# Entry Point
try:
    if sendDiscoverUDP() == None:
        raise Exception("Get no connection to server!")
    sendThread = threading.Thread(target=socketThread, args=(chatWriter, ))
    recvThread = threading.Thread(target=socketThread, args=(chatListener, ))

    sendThread.start()
    recvThread.start()

except Exception as error:
    print("Error!")
    print(error)

finally:
    sendThread.join()
    recvThread.join()
    print("Alles sauber aufgeräumt!")