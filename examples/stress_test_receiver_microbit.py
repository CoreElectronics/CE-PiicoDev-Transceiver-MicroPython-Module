import radio
from utime import sleep_ms

i=0
error = 0
value_prev = 0
success = 0
value = 0
while value < 250:
    data = radio.receive_bytes()
    if data is not None:
        value = int.from_bytes(data, "big")
        i = i + 1
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