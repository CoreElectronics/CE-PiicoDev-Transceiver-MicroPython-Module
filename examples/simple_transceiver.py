# Demonstrate an simple transceiver
# This script transmits and receives data.
# The transmitted data is an incrementing counter
# The received data is assumed to be a number. When the number
# is a multiple of five, a message is displayed. This proves we
# can receive data and do something with it.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

radio = PiicoDev_Transceiver()

last_send = 0 # timestamp of the last transmission event
counter = 0   # counter increases every transmission even

while True:
    
    # Always check for incoming messages
    if radio.receive():
        data = radio.message
        print('Received data:', data)
        
        # Do something with the received data
        if data % 5 == 0:
            print(data, 'is a multiple of 5')
        
    # Periodically send a unique value every second
    if ticks_ms() - last_send > 1000:
        last_send = ticks_ms() # update the timestamp
        radio.send( counter )  # send the number
        counter += 1           # increment the control variable
        
    sleep_ms(100)

