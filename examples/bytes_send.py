# This example works with the bytes_receive.py example
#
# pack() multiple data types into a single message payload
# For the receiver to make sense of the data, it will need to
# unpack() the data using the same format string.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from struct import *

radio = PiicoDev_Transceiver()

# pack format string: ">blf9s"
# > forces big-endian byte order
# b is a signed char (1 byte)
# l is a signed long (4 bytes)
# f is a float (4 bytes).
# 9s is a 9-character string
# For more information, refer to: https://docs.python.org/3/library/struct.html

data = pack(">blf9s", -127, 2_147_483_647, 3.14159265359, 'a string!')
radio.send_bytes(data)
