from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module



i=-400000000

radio.set_rfm69_register(0x29, 219)
sleep_ms(50)

while i > -4000000000:
    i-=1
    sleep_ms(10)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP',i) # biggest length before problems
    radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRST', address=3)
#     radio.send('abcdefghijklmnopqrstuvwxyz01234',i)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWQYZabcdefghijklmnopqrstuvwxyz0123456789',i)
    print('RFM_REG:' + str(radio.get_rfm69_register(0x29)))
    sleep_ms(50)
    