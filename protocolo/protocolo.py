import socket


class Protocolo():
    HEADERSIZE = 512
    PORT = 8844
    ip = "192.168.0.100"
    trans = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __init__(self, _ip):
        self.ip = _ip

    def __comandoSimples(self,str:cmd,int:format):
        ret = "falha"
        try:
            self.trans.connect((self.ip,self.PORT))
            msg = bytes(cmd,"utf-8")
            resposta_bytes = self.trans.recv(self.HEADERSIZE)
            resposta = resposta_bytes.decode('utf-8')
            
            pass
        except Exception as e:
            pass
        return ret
"""




s.connect((IP, PORT))

msg = "CMD0001,1,5,199,0,0"
s.send(bytes(msg,"utf-8"))

r_msg = s.recv(512)
print(f"{r_msg.decode('utf-8')}")
"""