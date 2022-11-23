from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

radio = PiicoDev_Radio()

def delta():
    return str(ticks_ms() - start_time)

i = 0
key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP'
value_prev=0
errors=0
successes=0
start_time = ticks_ms()
while i < 1000:
    i += 1
    print(delta() + ' SEND:'+ str(i))
    radio.send(key,i) # 3 seconds
    print(delta() + ' SENT')
    sleep_ms(200)
    if radio.receive():
        print(radio.key)
        print(radio.value)
        if (radio.value != value_prev + 1 or not radio.key == key) and i > 2:
            print('ERROR')
            errors += 1
        else:
            successes +=1
        value_prev = radio.value
#     sleep_ms(400)
error_rate = (errors / (errors + successes)) * 100
print('Error Rate: ' + str(error_rate) + '%')

