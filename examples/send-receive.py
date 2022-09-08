from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

radio.on()

while True:
    radio.led = 1
    sleep_ms(5000)
    radio.message = 'hellozworld\r '
    sleep_ms(1000)
    received_message = radio.message
    print(received_message)
    sleep_ms(2000)