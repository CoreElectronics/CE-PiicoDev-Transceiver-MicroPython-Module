from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

SPEED=1

radio = PiicoDev_Transceiver(radio_address=2, speed=SPEED, channel=0)

while True:
    if radio.receive():
        if radio.type == 3:
            print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.message) + " RSSI:" + str(radio.rssi))
            radio.send(radio.message)
        else:
            print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.value) + ':' + str(radio.key) + " RSSI:" + str(radio.rssi))
            radio.send(radio.key, radio.value)
    sleep_ms(5)