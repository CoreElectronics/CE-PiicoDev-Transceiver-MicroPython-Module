# Demonstrate how to use the send() command
# send() will accept strings, values and a "named value" which
# is a string-value pair.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver()

### Send text messages
radio.send("Hello, World!")
sleep_ms(1000)

### Send numeric values (integer and floating point accepted)
radio.send(123)
sleep_ms(1000)

### Send named values. Useful for labelling data from different sources
radio.send('temperature[degC]', 25.0)
sleep_ms(100)
radio.send('pressure[kPa]', 101.325)
sleep_ms(1000)

### Demo: Generate and send a sine wave
from math import sin
x = 0 # initialise a control variable
while True:
    y = sin(x)                 # generate a new number
    radio.send('my number', y) # send the number
    x += 0.2                   # increment the control variable
    sleep_ms(50)
