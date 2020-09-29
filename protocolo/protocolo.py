import socket
import datetime
import libscrc
import os



class Protocolo():
    HEADERSIZE = 1024
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

    def fileExist(self, nome):
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
        #print(msg)
        if msg != "RSP1003":
            return ret

        msg = self._comandoSimples(f"CMD1001/{nome},0,0,1",False,close=False,conect=False)
        #print(msg[:7])
        if msg[:7] != "RSP1001":
            return ret

        index = 1

        while msg != "RSP10020,ffff,EOF":
            msg = self._comandoSimples(f"CMD1002{index}",False,close=False,conect=False)           
            if msg != "RSP10020,ffff,EOF":
                valor = self._tratamentoString(msg)
                if valor > 0:
                    ret.append(self._stringTrocaQuebraL(msg[valor:]))
                    index+=1
                else:
                    return ['falha crc']

        msg = self._comandoSimples("CMD1003",False,conect=False)
        #print(msg)
        if msg != "RSP1003":
            return ret
        return ret

    def enviaArquivo(self,nome,pasta):
        return self._estruturaArquivo(nome,pasta)

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

    def _tratamentoString(self,rcp:str):
        try:
            index = rcp.split(',')
            ponto = rcp.find(',',14)+1
            crc_ok = index[1].upper()
            #print (f'a mensagem é :{rcp}')
            #print(f" format : {rcp[ponto:]}")
            #print(f'crc lido: {crc_ok}')
            crc_lido = self._crc16(rcp[ponto:])
            #print(f'crc calc: {crc_lido}')       
            if crc_ok != crc_lido:
                return -1
            else:
                return ponto
        except:
            return -1

    def _stringTrocaQuebraL(self,dados:str,decode=True):
        ret = ""
        result = ""
        for x in dados:
            temp=x
            #"""
            if decode:
                if x == '':
                    temp=''
                if x == '':
                    temp = u'\u000A'
            else:
                if x == u'\u000A':
                    temp = ''
            #"""
            result+=temp
        return result

    def _estruturaArquivo(self,nome,pasta):
        colecao = []
        arquivo = open(pasta+nome,'r')
        dados = self._stringTrocaQuebraL(arquivo.read(),decode=False)
        #dados = arquivo.read()
        #print(dados)
        #tamanho = os.path.getsize(os.path.join(pasta,nome))
        tamanho = len(dados)
        #print(f'tipo: {type(dados)}')
        #print(tamanho)
        #"""
        loops = int(tamanho/512)
        print(f'loops: {loops}')
        resto = int(tamanho%512)
        print(f'resto: {resto}')
        nomeArquivo = nome

        if nome.find(".xml")>0:
            nomeArquivo = "WLConfig.xml"

        colecao.append(f'CMD1001{nomeArquivo},1,{str(tamanho)},0')
       
        for x in range(loops):
            temp = dados[x*512:(x*512)+512]
            print(temp)
            size = str(len(temp))
            print(size)
            crc = self._crc16(temp)
            print(crc)
            colecao.append(f'CMD1002{size},{crc},{x+1},{temp}')
        temp = dados[tamanho-resto:]
        size = str(len(temp))
        print(size)
        crc = self._crc16(temp)
        colecao.append(f'CMD1002{size},{crc},{x+1},{temp}')

        return colecao
        #"""
        #return dados
        


    def _crc16(self,dados):
        b = bytes(dados,'ASCII')
        valor= str(hex(libscrc.modbus(b))).upper()[2:]
        hi = valor[2:]
        lo = valor[:2]
        return hi+lo