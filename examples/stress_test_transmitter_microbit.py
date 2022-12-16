import radio
from utime import sleep_ms

i=0
while i < 255:
    i+=1
    sleep_ms(10)
    radio.send_bytes(i.to_bytes(1, 'big'))
    sleep_ms(50)
