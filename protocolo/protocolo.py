import socket

HEADERSIZE = 10
IP = "192.168.0.100"
PORT = 8844

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP, PORT))

msg = "CMD0001,1,5,199,0,0"
s.send(bytes(msg,"utf-8"))

r_msg = s.recv(512)
print(f"{r_msg.decode('utf-8')}")