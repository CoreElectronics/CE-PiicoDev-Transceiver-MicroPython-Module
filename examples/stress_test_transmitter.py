from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module



i=0

#radio.set_rfm69_register(0x29, 228)
sleep_ms(50)

while i < 1000:
    i+=1
    sleep_ms(10)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP',i) # biggest length before problems
    radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRST', i, address=0)
#     radio.send('abcdefghijklmnopqrstuvwxyz01234',i)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWQYZabcdefghijklmnopqrstuvwxyz0123456789',i)
    print('RFM_REG:' + str(radio.get_rfm69_register(0x29)))
    sleep_ms(3000)
    