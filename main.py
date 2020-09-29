from protocolo.protocolo import Protocolo
import os

dxm = Protocolo("192.168.0.100")
#"""
arrei = dxm.enviaArquivo("teste.sb","")
arquivo = open("output.sb",'w')

for c in arrei:
    arquivo.write(c+'\r')

arquivo.close()
"""
arrei = dxm.getFile("OEE.sb")
temp = ""
for c in arrei:
    temp+=c
arquivo = open("teste.sb",'w')
arquivo.write(temp)
arquivo.close()
"""
