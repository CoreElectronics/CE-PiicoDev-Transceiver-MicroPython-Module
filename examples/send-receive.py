from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

# Notes from Graham:
#ToDo - Test to see what happens when we have the same address for all devices.
# We need this to be the same as the microbit
# We need to make it so that we have a huge class that allows us to support every feature.
# for example.  A default encryption key, can be overwritten by the micropython driver
# No settings should be hard coded.  Not every setting needs to be controled
# Don't worry about sleep mode
# We don't need acknowledgements.  We are using a broadcast system.
# Micropython driver is sending text by defualt.  Getas treated like bytearray through the smart module
# just get them to send a string (same as micro:bit)
# definately use the "group" feature in the microbit
# Channel / address / group
# We need to make our own checksum (check if hope RF does checksum - check that someone else has already done it or not
# See if can change data rate?
# Go through the hope rf datasheet - make a list of what settings work through the filix driver.
# Group, channel etc is all micropythoin - we don't need to send that through to the SMART module
# Is there data for my address? function
# Is there dtaa available in my group function
# is data available for the channel?
# State machine -> new data received
# Make sure transmitters can't flood networks.  Make the delay configurable.
# Use a function called newData() that decides if new data is available for  the given scope.
# On the readme, use words like whisper, chat and broadcasting

#Current ststus - send data from micropython.  Send to arduino running on vm.  Still need to do Arduino -> micropython link

send_string = 'hello world'

radio.on()

while True:
    radio.led = 1
    sleep_ms(5000)
    radio.message = send_string
    sleep_ms(1000)
    radio.messageLength = len(send_string)
    #received_message = radio.message
    received_bytes = radio.receive_bytes()
    #print(received_message)
    print(received_bytes)
    sleep_ms(2000)