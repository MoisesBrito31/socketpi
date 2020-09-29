from protocolo.protocolo import Protocolo
import os

dxm = Protocolo("192.168.0.100")

result = dxm.enviaArquivo("OEE.sb","")

print(result)