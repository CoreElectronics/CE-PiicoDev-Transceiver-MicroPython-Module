from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

radio = PiicoDev_Radio(radio_address=2, channel=0)

i = 5
key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRS'
#key = 'abcdefghijklmn'
value_prev=0
errors=0
successes=0
firmware = radio.firmware
print('ID:             ' + str(radio.whoami))
print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
print('Tx Power:       ' + str(int(radio.tx_power)))
print('Radio Address   ' + str(radio.radio_address))
print('Channel:        ' + str(radio.channel))
sleep_ms(3000)
radio_state = True
radio.on()


while i < 1000:
    print(radio_state)
    i += 1
    radio.send(key,i,address=0)
    sleep_ms(3000)  #200
    if radio.receive():
        print(radio.key)
        print(radio.value)
        if (radio.value != value_prev + 1 or not radio.key == key) and i > 2:
            print('ERROR')
            errors += 1
        else:
            successes +=1
            print('SUCCESS')
        value_prev = radio.value
    sleep_ms(100)
        
error_rate = (errors / (errors + successes)) * 100
print('Error Rate: ' + str(error_rate) + '%')
