# Demonstrate how to use the send() command
# send() will accept strings, values, and "named values" which
# are string,value pairs.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver()

# Text messages
radio.send("Hello, World!")
sleep_ms(1000)

# Numbers (integer or floating point)
radio.send(123)
sleep_ms(1000)

# Named Values
named_data = ('temperature[degC]', 25.0)
radio.send(named_data)
sleep_ms(100)

named_data = ('humidity[%]', 60.0)
radio.send(named_data)
sleep_ms(1000)



### Demo: Generate and send a sine wave
from math import sin
x = 0 # initialise a control variable
while True:
    y = sin(x)                 # generate a new number
    radio.send( ('my number', y) ) # send the number
    x += 0.2                   # increment the control variable
    sleep_ms(100)
