#!/usr/bin/python3
import socket
import sys
import os.path
from urllib.parse import urlparse
import re


TCP_IP = '127.0.0.1'
TCP_PORT = 25
BUFFER_SIZE = 1024



#  entry point:
try:
    # argument #1 sender andress
    # argument #2 receiver adress
    # argument #3 subject
    if len(sys.argv) != (1 + 3):
        raise Exception("Invalid number of Arguments")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))

    sock.send(b"HELO myName")




except:

    print("Ein Fehler ist aufgetreten")
    import traceback
    traceback.print_exc()

finally:
    sock.close()