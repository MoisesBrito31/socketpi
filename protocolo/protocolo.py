import socket
import datetime


class Protocolo():
    HEADERSIZE = 512
    PORT = 8844
    ip = "192.168.0.100"
    trans = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def __init__(self, _ip):
        self.ip = _ip

    def getMAC(self):
        return self._comandoSimples("CMD0112",True)

    def getRelogio(self):
        ret = datetime.datetime(2000,1,1,0,0,0)
        try:
            resposta = self._comandoSimples("CMD0102",True)
            ret = datetime.datetime.strptime(resposta,'%Y-%m-%d %H:%M:%S')
            fuso = datetime.datetime(ret.year,ret.month,ret.day,ret.hour-3,ret.minute,ret.second)          
            return fuso
        except:
            return ret

    def setRelogio(self):
        now = datetime.datetime.now()
        cmd = f'CMD0101{now.year},{now.month},{now.day},{now.hour+3},{now.minute},{now.second}'
        ret = self._comandoSimples(cmd,False)
        if ret == 'RSP0101':
            return True
        else:
            return False

    def getSerialumber(self):
        return self._comandoSimples("CMD0113",True)

    def reset(self):
        return self._comandoSemRetorno("CMD0200")

    def reboot(self):
        return self._comandoSemRetorno("CMD020055S")

    def travar(self):
        resp = self._comandoSimples("CMD0449",False,close=False)        
        if resp != "RSP04490":
            if resp == "RSP04491":
                return True
            return False
        resp = self._comandoSimples("CMD045055YmV0aW01MTY=",False,conect=False)
        if resp != "RSP0450":
            return False
        return True
        
    def destravar(self):
        resp = self._comandoSimples("CMD0449",False,close=False)  
        if resp != "RSP04491":
            if resp == "RSP04490":
                return True
            return False
        resp = self._comandoSimples("CMD0451YmV0aW01MTY=",False,conect=False,close=False)
        if resp != "RSP0451":
            return False
        resp = self._comandoSimples("CMD0452",False,conect=False)
        if resp != "RSP0452":
            return False
        return True

    def fileExit(self, nome):
        msg = self._comandoSimples(f"CMD1005 {nome}",True)
        if msg == '1':
            return True
        else:
            return False

    def deleteFile(self, nome):
        return self._comandoSemRetorno(f"CMD1006 {nome}")

    def getFile(self, nome):
        ret = []
        msg = self._comandoSimples("CMD1003",False,close=False)
        print(msg)
        if msg != "RSP1003":
            return ret

        msg = self._comandoSimples(f"CMD1001/{nome},0,0,1",False,close=False,conect=False)
        print(msg)
        if msg[:7] != "RSP1001":
            return ret

        index = 1
        auxiliar = ""

        while msg != "RSP10020,ffff,EOF":
            msg = self._comandoSimples(f"CMD1002{index}",False,close=False,conect=False)
            print(msg)
            if msg != "RSP10020,ffff,EOF":
                #faz tratamento da string
                if msg != "falha":
                    ret.append(msg)
                    index+=1

        msg = self._comandoSimples("CMD1003",False,conect=False)
        print(msg)
        if msg != "RSP1003":
            return ret
        return ret

    def _comandoSimples(self,cmd,format,close=True,conect=True):
        ret = "falha"
        try:
            if conect:
                self.trans.connect((self.ip,self.PORT))
            msg = bytes(cmd,"utf-8")
            self.trans.send(msg)
            resposta_bytes = self.trans.recv(self.HEADERSIZE)
            resposta = resposta_bytes.decode('utf-8')
            if format:
                ret = resposta[7:]
            else:
                ret = resposta
            if close:
                self.trans.close() 
        except Exception as e:
            return f'{ret} {str(e)}'
        return ret

    def _comandoSemRetorno(self,cmd):
        try:
            self.trans.connect((self.ip,self.PORT))
            msg = bytes(cmd,"utf-8")
            self.trans.send(msg)
            self.trans.close() 
            return True
        except:
            return False
