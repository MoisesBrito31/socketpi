from protocolo.mapa import Mapa

class Xml():
    pasta = ""
    nomeArquivo = ""
    arquivo = ""
    mapa = Mapa.carrega("base","base.mapa")

    def __init__(self, pasta="mapas",nomeArquivo="base.mapa",nome="base", mapa=Mapa.carrega("base","base.mapa")):
        self.mapa = mapa
        self.pasta=pasta
        self.nomeArquivo = nomeArquivo
        self._carregaXml()

    def _carregaXml(self):
        file = open(f'{self.pasta}/{self.nomeArquivo}','r')
        self.arquivo = file.read()
        file.close()


