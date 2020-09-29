



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
