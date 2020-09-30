from protocolo.protocolo import Protocolo
from protocolo.mapa import Mapa, Evento, Reg, Bloco
from protocolo.xml import Xml
import os
import datetime

dxm = Protocolo("192.168.0.100")

x = Xml(mapa=Mapa.carrega("mapas2/","amb.mapa"))
x._carregaXml()
m = Mapa.carrega("mapas2/","amb.mapa")
m.pasta = "mapas2/"
m.nomeArquivo = "amb.mapa"
m.salva()
print(m.qntEquip)
#x._compilaArquivo()
