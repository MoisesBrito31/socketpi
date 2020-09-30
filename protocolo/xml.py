from protocolo.mapa import Mapa

class Xml():
    pasta = ""
    nomeArquivo = ""
    arquivo = ""
    mapa = Mapa.carrega("base","base.mapa")
    buffer = []

    def __init__(self, pasta="",nomeArquivo="DXM_OEE.xml",nome="base", mapa=Mapa.carrega("base","base.mapa")):
        self.mapa = mapa
        self.pasta=pasta
        self.nomeArquivo = nomeArquivo
        self._carregaXml()

    def _carregaXml(self):
        file = open(f'{self.pasta}{self.nomeArquivo}','r')
        self.arquivo = file.read()
        file.close()

    def salvaArquivo(self):
        file = open(f'{self.pasta}{self.nomeArquivo}','w')
        for s in self.buffer:
            file.write(s)
        file.close()

    def subArquivoIni(self):
        indexini = self.arquivo.find("<rtu_read>")
        if indexini>0 :
            return f'{self.arquivo[:indexini]}\r <rtu_read> \r'
        else:
            return 'falha'

    def subArquivoRegs(self):
        ret = ''
        for b in self.mapa.blocos:
            for r in b.regList:
                ret+=f'{r.reg}\r'
        return ret

    def _compilaArquivo(self):
        temp1 = self.subArquivoIni()
        temp2 = self.subArquivoRegs()
        print(temp2)

   

    



