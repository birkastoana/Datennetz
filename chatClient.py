#!/usr/bin/python3

import os, sys, threading, re, socket, time, select, ctypes

TCP_IP = ''
TCP_PORT = 25
BUFFER_SIZE = 1024
UDP_IP = '255.255.255.255'
UDP_PORT = 3333
TERMINATOR = "\r\n"
def sendDiscoverUDP():
    try:
        udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # udpSock.connect((UDP_IP, UDP_PORT))
        udpSock.settimeout(5)
        udpSock.sendto(b'DISCOVER', ("<broadcast>", 3333))
        response = udpSock.recv(BUFFER_SIZE)
        response = re.match(b"ADDR (\d+.\d+.\d+.\d+):(\d+)", response)
        TCP_IP = response[1].decode()
        TCP_PORT = int(response[2].decode())
        return TCP_IP, TCP_PORT
    except:
        return None
    finally:
        udpSock.close()

def msgInterpreter(msg):
    try:
        msg = msg.decode()
        status = int(msg[:3])
        if status > 299:
            print("Error!!")
            print(msg)
    except:
        print("\n", msg)

class chatReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        r,w,e = select.select([self.sock], [], [])
        while not self.kill_received:
            try:
                recvMsg = self.sock.recv(BUFFER_SIZE)
                if len(recvMsg) > 0:
                    msgInterpreter(recvMsg)

            except :
                continue

class pingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # A flag to notify the thread that it should finish up and exit
        self.kill_received = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = ""
    def run(self):
        n = 0
        while not self.kill_received:
            n += 1
            if n > 10:
                self.sock.send(("PING " + self.username + TERMINATOR).encode())
                n = 0
            time.sleep(1)

def main(args):
    try:
        TCP_IP, TCP_PORT = sendDiscoverUDP()
        if TCP_IP == None:
            raise Exception("Get no connection to server!")
    except Exception as error:
        print("Error!")
        print(error)
    else:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("connect to ", TCP_IP, ":", TCP_PORT)
            sock.connect((TCP_IP, TCP_PORT))
            username = input("Choose your Username: ")
            connectMsg = "CONNECT " + username + TERMINATOR
            sock.send(connectMsg.encode())
            statusMsg = sock.recv(BUFFER_SIZE)
            status = int(statusMsg[:3])
            if status != 200:
                raise Exception(statusMsg)
            print("Hi ", username, "! Feel free to start messaging!\nYou can quit the Chat by hitting ctrl+c!")
        except Exception as error:
            print("Error: Cannot connect to Chat-Server")
            print(error)
        else:
            thread = chatReceiver()
            pThread = pingThread()
            thread.start()
            thread.sock = sock
            pThread.start()
            pThread.sock = sock
            pThread.username = username
            while thread.kill_received != True:
                try:
                    sendMsg = input(("<you> "))
                    sock.send(("MSG " + sendMsg + TERMINATOR).encode())
                except KeyboardInterrupt:
                    print( "\nLogging out")
                    pThread.kill_received = True
                    thread.kill_received = True
                    closeMsg = "DISCONNECT " + username + TERMINATOR
                    sock.send(closeMsg.encode())
                    thread.join()
                    sock.close()
                    print("Logged out successfull!")

if __name__ == '__main__':
    main(sys.argv)