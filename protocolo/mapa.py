from datetime import datetime
import pickle
import os

class Evento():
    id = 0
    end = datetime.now()
    nome = 'sem nome'
    regControle = 91
    start = datetime.now()
    on = 1
    off = 0
    exclude = 0
    days = "SMTWHFR"

    def __init__(self,nome:str,start:datetime,id=0,regControle=91,on=1,off=1,exclude=0,days="SMTWHFR"):
        self.id = id
        self.nome = nome
        self.regControle = regControle
        self.start = start
        self.end = datetime(start.year,start.month,start.day,start.hour,start.minute,start.second+1)
        self.on = 1
        self.off = 0
        self.exclude = exclude
        self.days = days

    def getXml(self):
        return f'<event end=\"{str(self.end.hour)}:{str(self.end.minute)}\" name=\"{self.nome}\" reg=\"{str(self.regControle)}\" start=\"{str(self.start.hour)}:{str(self.start.minute)}\" on=\"{str(self.on)}\" exclude=\"{str(self.exclude)}\" days=\"{self.days}\" off=\"{str(self.off)}\" />'

class Bloco():
    nome = "sem nome"
    regList = []

    def __init__(self,nome,regList):
        self.nome= nome
        self.regList = regList

class Reg():
    nome = ""
    id = 0
    slaveID = 1
    reg = 1
    ciclo = 1000
    dword = False
    ativo = True

    def __init__(self,reg,ciclo=1000,dword=False,ativo=True,id=0,slaveID=1,nome=""):
        self.nome = nome
        self.id = id
        self.slaveID = slaveID
        self.reg = reg
        self.ciclo = ciclo
        self.dword = dword
        self.ativo = ativo

class Mapa():
    nome = ""
    pasta = ""
    nomeArquivo = ""
    blocos = []
    turnos = []
    qntEquip = 0
    arquivo = ""

    def __init__(self, nome, nomeArquivo,pasta="",blocos=[],turnos=[],qntEquip=0):
        self.pasta = pasta
        self.nome = nome
        self.nomeArquivo = nomeArquivo
        self.blocos =blocos
        self.turnos = turnos
        self.qntEquip = qntEquip

    @staticmethod
    def carrega(pasta,nomeArquivo):
        try:
            arquivo = open(f'{pasta}{nomeArquivo}','rb')
            pic = pickle.load(arquivo)
            arquivo.close()
            return pic

        except Exception as e:
            print(str(e))

    def salva(self):
        try:
            try:
                os.mkdir(self.pasta)
            except:
                pass
            arquivo = open(f'{self.pasta}{self.nomeArquivo}','wb')
            pickle.dump(self,arquivo)
            arquivo.close()

        except Exception as e:
            print(str(e))

    def alteraQtdEquip(self,num:int):
        if num > self.qntEquip:
            regs =[]
            a = Reg(17)
            for x in range(3):
                regs.append(a)
            for x in range(num-self.qntEquip):
                b = Bloco(f'equipamento {x}',regs)
                self.blocos.append(b)
            self.qntEquip = len(self.blocos)
            self.salva()
            return True
        if num < self.qntEquip:
            self.blocos = self.blocos[:num]
            self.qntEquip = len(self.blocos)
            self.salva()
            return True
        return False

    def alteraNomeEquip(self,nomes:list):
        for x in range(len(nomes)):
            self.blocos[x].nome = nomes[x]