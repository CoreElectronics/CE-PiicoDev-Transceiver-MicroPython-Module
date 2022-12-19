from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from struct import *

radio = PiicoDev_Transceiver(radio_address=2, speed=3)

while True:
    if radio.receive_bytes():
        value = unpack('>i', radio.received_bytes)[0]
        print(value)
    sleep_ms(5)
