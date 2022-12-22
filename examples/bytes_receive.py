# This example works with the bytes_send.py example
#
# unpack() multiple data types from a single message payload
# For the receiver to make sense of the data, it must
# unpack() the data using the same format string that the transmitter used
# to pack() the data.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from struct import *

radio = PiicoDev_Transceiver()

while True:
    if radio.receive_bytes():
        b,H,l,f, message = unpack('>bHlf9s', radio.received_bytes)
        print("signed char... : ", b)
        print("unsigned short : " , H)
        print("long.......... : ", l)
        print("float......... : ", f)
        print("string........ : ", message)
        print("")
    sleep_ms(5)
