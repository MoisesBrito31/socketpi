from protocolo.protocolo import Protocolo
from protocolo.mapa import Mapa, Evento, Reg, Bloco
from protocolo.xml import Xml
import os
import datetime

dxm = Protocolo("192.168.0.100")

map = Mapa(inicia=True)
#x = Xml(Mapa.carrega("mapas2/","amb.mapa"),nomeArquivo='base.xml')
x = Xml(map,nomeArquivo='base.xml')
x._carregaXml()
x.salvaArquivo()
m = x.mapa


x._compilaArquivo()
