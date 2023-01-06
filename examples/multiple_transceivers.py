# Demonstrate how to use the send() command
# send() will accept strings, values, and "named values" which
# are string,value pairs.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from math import sin

# Initialise two separate radios
transmitter = PiicoDev_Transceiver(id=[0,0,0,0])
receiver    = PiicoDev_Transceiver(id=[1,0,0,0])

x = 0

while True:
    # TRANSMIT a new value from one Transceiver
    y = sin(x)                           # generate a new number
    transmitter.send( ('sine wave', y) ) # send the number
    x += 0.2                             # increment the control variable
        
    sleep_ms(100)
    
    # RECEIVE any incoming messages and print
    if receiver.receive():
        message = receiver.message
        print(message)