from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver(group=0)

while True:
    if radio.receive():
        message = radio.message
        print(message)
        radio.send(message) # echo back the same message

    sleep_ms(50)