# Listen for LED control messages
# Valid messages set the state of the on-board LED

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from time import ticks_ms
from random import randrange

radio = PiicoDev_Transceiver(radio_address=3, group=15)

duration = 1000
period = 3000
last_flash = randrange(0, period)
state = False


def tune_flash(ref):
    global last_flash, state
    now = ticks_ms()
    err = ref - (now - last_flash)
    if abs(err) > 50:
        if state is True: # I'm ahead of another firefly
            last_flash -= 0.2 * err
        if state is False: # I'm lagging behind another firefly
            last_flash += 0.1 * err

while True:
    if radio.receive():
        message = radio.message
        print(message)
        tune_flash(message)
    
    now = ticks_ms()
    if state is False and now - last_flash > period:
        radio.led = True
        state = True
        last_flash = now
        # Wait some time before sending the timestamp (prevents RF collisions)
        wait_time = randrange(0,duration)
        sleep_ms(wait_time)
        radio.send(wait_time)
        
    if state is True and now - last_flash > duration:
        radio.led = False
        state = False
        
    sleep_ms(50)