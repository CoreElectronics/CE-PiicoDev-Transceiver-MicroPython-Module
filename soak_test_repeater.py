from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

i = 0
key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP'
# key = 'abcd'
# key = 'abcdefghijklmno'
while True:
#    if radio.receive():
    i = i + 1
#         print(str(radio.key) + ":" + str(radio.rssi))
    # sleep_ms(20)
#         radio.send(radio.key, radio.value)
    radio.send(key, i)
    sleep_ms(10000)