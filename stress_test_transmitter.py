from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

i=0
while i < 255:
    i+=1
    sleep_ms(10)
    radio.send("abcdefghijklmnopqrstuvwxyz123",i)
    sleep_ms(50)
    