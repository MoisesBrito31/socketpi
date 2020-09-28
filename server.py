import socket
import time
import pickle


HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IP,PORT))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Conection from {address} has been established!")

    msg = "Welcome to the server!"
    msg= f'{len(msg):<{HEADERSIZE}}' + msg

    clientsocket.send(bytes(msg,"utf-8")) 