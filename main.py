from protocolo.protocolo import Protocolo
from protocolo.mapa import Mapa, Evento, Reg, Bloco
from protocolo.xml import Xml
import os
import datetime
from threading import Thread
from time import sleep
from pyModbusTCP.client import ModbusClient as Modbus 

dxm = Modbus(host='192.168.0.100',port=502)
dxm.open()

print (dxm.read_holding_registers(5,2))
