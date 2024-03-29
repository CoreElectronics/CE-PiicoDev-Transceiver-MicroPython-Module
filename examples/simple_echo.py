# Listen for any message and print to the shell

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver()

while True:
    if radio.receive():
        message = radio.message
        print(message)
        radio.send(message) # echo back the same message - useful for debugging!

    sleep_ms(50)