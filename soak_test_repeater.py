from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

while True:
    if radio.receive():
        radio.send(radio.key, radio.value)
    sleep_ms(10)
