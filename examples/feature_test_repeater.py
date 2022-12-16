from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

RADIO_ADDRESS = 33
SPEED = 2
CHANNEL=0

radio = PiicoDev_Transceiver(radio_address=RADIO_ADDRESS, speed=SPEED, channel=CHANNEL)

while True:
    if radio.receive():
        if radio.type == 3:
            print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.message) + " RSSI:" + str(radio.rssi))
            radio.send(radio.message)
        else:
            print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.value) + ':' + str(radio.key) + " RSSI:" + str(radio.rssi))
            radio.send(radio.key, radio.value)
    sleep_ms(5)