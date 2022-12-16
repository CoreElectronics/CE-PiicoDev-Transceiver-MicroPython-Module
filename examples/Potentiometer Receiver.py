from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

while True:
    firmware = radio.firmware
    radio.led = 1
    sleep_ms(50)
    incoming_datagram = radio.receive()
    if incoming_datagram != 0:
        print('incoming_datagram' + str(incoming_datagram))
        print('value: ' + str(incoming_datagram[2]))
    sleep_ms(25)
