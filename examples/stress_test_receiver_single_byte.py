from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

i=0
error = 0
value_prev = 0
success = 0
value = 0
while value < 250:
    sleep_ms(10)
    value = radio.receive_byte()
    if value != 0:
        i=i+1
        if value > value_prev + 1:
            error += 1
            print('error')
        else:
            success += 1
        value_prev = value
        print(value)
    sleep_ms(10)

error_rate = (error / (error + success)) * 100

print('Error Rate: ' + str(error_rate) + '%')