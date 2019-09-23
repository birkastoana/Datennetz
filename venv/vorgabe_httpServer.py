#!/usr/bin/python3

# Wird benÃ¶tigt, damit wir Sockets verwenden kÃ¶nnen
import socket

TCP_IP = 'localhost'
TCP_PORT = 2500
BUFFER_SIZE = 1024

# Wir erzeugen einen neuen Stream Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wir binden den Socket an eine IP und einen Port,
# und machen ihn dadurch zu einem Server-Socket
sock.bind((TCP_IP, TCP_PORT))

# Wir warten auf eingehende Verbindungen
sock.listen()

# Wir akzeptieren eine eingehende Verbindung
clientsock, clientaddr = sock.accept()
print('Eingehende Verbindung von ', clientaddr)

while True:
    # Wir empfangen Daten vom Client
    data = clientsock.recv(BUFFER_SIZE)

    # Wenn die Verbindung geschlossen wurde, ist data leer
    if not data:
        break

    print("Empfangene Daten: ", data)

    # Wir senden die Daten zurÃ¼ck an den Client
    clientsock.send(data)

# Wir geben alle Ressourcen wieder frei
clientsock.close()
sock.close()