from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

i=0.0
error = 0
value_prev = 0
success = 0
value = 0
compare_string = 'abcdefghijklmnopqrstuvwxyz123'
while value < 250:
    sleep_ms(10)
    data = radio.receive()
    if data != 0:
        value = data[2]
        message = str(data[4],'utf8')
        print('---')
        print(message)
        ascii_values = []
        for character in message:
            ascii_values.append(ord(character))
        print(ascii_values)
        print('--')
        print(compare_string)
        ascii_values_compare = []
        for character_compare in compare_string:
            ascii_values_compare.append(ord(character_compare))
        print(ascii_values_compare)
        print('-')
        i=i+1
        if value > value_prev + 1.1 or not message == compare_string:
            error += 1
            print('error')
        else:
            success += 1
        if value > value_prev + 1.1:
            print('number problem')
        if not message == compare_string:
            print('pot problem')
        value_prev = value
        print(value)
    sleep_ms(10)

error_rate = (error / (error + success)) * 100

print('Error Rate: ' + str(error_rate) + '%')
