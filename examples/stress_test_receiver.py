from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

i=0.0
error = 0
value_prev = 0
success = 0
value = 0
compare_string = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP'
radio_state = True
while value < 250:
    sleep_ms(10)
    print('radio state:'+str(radio_state))
    if radio.receive():
#         value = data[2]
        print('radio received message')
        print(radio.value)
        key = radio.key
        ascii_values = []
        for character in key:
            ascii_values.append(ord(character))
#         print(ascii_values)
        print(compare_string)
        ascii_values_compare = []
        for character_compare in compare_string:
            ascii_values_compare.append(ord(character_compare))
#         print(ascii_values_compare)
        print('-')
        i=i+1
        if value > value_prev + 1.1 or not key == compare_string:
            error += 1
            print('error')
        else:
            success += 1
        if value > value_prev + 1.1:
            print('number problem')
        if not key == compare_string:
            print('text problem')
        value_prev = value
        print(value)
    if radio_state == True:
        radio.off()
        radio_state = False
    else:
        radio.on()
        radio_state = True
    sleep_ms(3000)

error_rate = (error / (error + success)) * 100

print('Error Rate: ' + str(error_rate) + '%')
