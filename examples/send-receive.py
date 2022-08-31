from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

while True:
    radio.on()
    radio.led = 1 
    radio.message = 'hello world'
    #received_message = radio.message
    #print(received_message)
    radio.off()
    sleep_ms(2000)