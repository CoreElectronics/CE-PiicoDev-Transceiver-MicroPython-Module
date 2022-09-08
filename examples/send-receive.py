from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

Current ststus - send data from micropython.  Send to arduino running on vm.  Still need to do Arduino -> micropython link

radio.on()

while True:
    radio.led = 1
    sleep_ms(5000)
    radio.message = 'h'
    sleep_ms(10);
    radio.message = 'i'
    sleep_ms(1000)
    radio.messageLength = 2
    received_message = radio.message
    print(received_message)
    sleep_ms(2000)