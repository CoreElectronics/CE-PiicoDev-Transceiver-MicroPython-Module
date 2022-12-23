from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver()

while True:
    if radio.receive():
        print(radio.message)

    sleep_ms(50)