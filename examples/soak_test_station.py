from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

debugging=False

radio = PiicoDev_Transceiver(radio_address=0, channel=0)

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

while i < 10000:
    i += 1
    radio.send(key,i,address=2)
    sleep_ms(200)  #200
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
