# This example works with the bytes_receive.py example
#
# pack() multiple data types into a single message payload
# For the receiver to make sense of the data, it will need to
# unpack() the data using the same format string.

from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from struct import *

radio = PiicoDev_Transceiver()

# pack format string: ">bHlf9s"
# > = force big-endian byte orderd
# b = signed char (1 byte)
# H = unsigned short (2 bytes)
# l = signed long (4 bytes)
# f = float (4 bytes).
# 9s = string with 9 characters
# For more information, refer to: https://docs.python.org/3/library/struct.html

data = pack(">bHlf9s", -127, 65535, 2_147_483_647, 3.14159265359, 'a string!')
radio.send_bytes(data)
sleep_ms(6)
