from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()

i=0.0
error = 0
value_prev = 0
success = 0
value = 0
message = ''
compare_string = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP'
while value < 250:
    sleep_ms(10)
    if radio.receive():
        print('                RSSI:' + str(radio.rssi))
        print('             Channel:' + str(radio.channel))
        print('                Type:' + str(radio.type))
        print('Source Radio Address:' + str(radio.source_radio_address ))
        print('                 Key:' + str(radio.key))
        print('               Value:' + str(radio.value))
        print('             Message:' + str(radio.message))
        
    sleep_ms(30)

error_rate = (error / (error + success)) * 100

print('Error Rate: ' + str(error_rate) + '%')
