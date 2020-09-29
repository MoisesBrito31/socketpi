from protocolo.protocolo import Protocolo
from protocolo.mapa import Mapa, Evento, Reg, Bloco
import os
import datetime

dxm = Protocolo("192.168.0.100")

#"""
e = Evento('primeiro turno',datetime.datetime(2020,9,30,15,30,0))
e2 = Evento('segundo turno',datetime.datetime(2020,9,30,17,30,0))

r = Reg(22,nome='contagem in')
r1 = Reg(23,nome='contagem out')
r2 = Reg(24,nome='status')

b = Bloco("maquina 1", [r,r1,r2])
b2 = Bloco("maquina 2",[r,r2])

m = Mapa("ambev","amb.mapa",blocos=[b,b2],turnos=[e,e2],qntEquip=2,pasta="mapas2")

m.salva()
print(m.qntEquip)
novo = int(input('digite um valor: '))
m.alteraQtdEquip(novo)
print(m.qntEquip)
#"""


print(m.qntEquip)
