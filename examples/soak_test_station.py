from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

debugging=False

radio = PiicoDev_Radio(radio_address=127, channel=0, debug=debugging)

i = 0
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
radio.tx_power = 21
print('radio.tx_power:' + str(radio.tx_power))
#radio.get_frequency()
#sleep_ms(1000)
radio.radio_frequency = 915
print(radio.radio_frequency)
radio.radio_frequency = 918
print(radio.radio_frequency)
radio.radio_frequency = 922
print(radio.radio_frequency)
radio.radio_frequency = 925
print(radio.radio_frequency)
radio.radio_frequency = 928
print(radio.radio_frequency)
radio.radio_frequency = 922
radio.speed = 2

while i < 10000:
    i += 1
    radio.send(key,i,address=0)
    #sleep_ms(1000)
    sleep_ms(100)  #200
    if radio.receive():
        if (radio.value != value_prev + 1 or not radio.key == key) and i > 2:
            print(radio.key + ':' + str(radio.value) + ':ERROR' + str(radio.rssi))
            errors += 1
        else:
            successes +=1
            print(radio.key + ':' + str(radio.value) + ':SUCCESS:' + str(radio.rssi))
        value_prev = radio.value
    sleep_ms(20)
    if debugging:
        sleep_ms(100)
        
error_rate = (errors / (errors + successes)) * 100
print('Error Rate: ' + str(error_rate) + '%')
