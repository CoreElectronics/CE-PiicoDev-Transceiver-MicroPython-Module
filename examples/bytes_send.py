from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from struct import *

radio = PiicoDev_Transceiver(radio_address=1, speed=3)
value = 0

while True:
    value += 1
    data = pack('>i', value)
    radio.send_bytes(data, address=2)
    sleep_ms(6)
