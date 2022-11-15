from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

i=-400000000
while i > -4000000000:
    i-=1
    sleep_ms(10)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP',i) # biggest length before problems
    radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRST', address=3) # why isn't the 's' being sent
#     radio.send('abcdefghijklmnopqrstuvwxyz01234',i)
#     radio.send('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWQYZabcdefghijklmnopqrstuvwxyz0123456789',i)
    sleep_ms(50)
    