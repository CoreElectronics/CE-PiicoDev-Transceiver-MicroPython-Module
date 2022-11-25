from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms
from time import ticks_ms

radio = PiicoDev_Radio()

i = 0
key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP'
value_prev=0
errors=0
successes=0
radio.rfm69_node_id = 1
radio.rfm69_network_id = 0
radio.rfm69_to_node_id = 1
radio_tx_power = -3
radio.tx_power = radio_tx_power
firmware = radio.firmware
print('ID:             ' + str(radio.whoami))
print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
print('Tx Power:       ' + str(int(radio.tx_power)))
print('Node ID:        ' + str(radio.rfm69_node_id))
print('Network ID:     ' + str(radio.rfm69_network_id))
print('To Node ID:     ' + str(radio.rfm69_to_node_id))
sleep_ms(3000)
radio_state = True
radio.on()


while i < 1000:
    print(radio_state)
    i += 1
    radio.send(key,i)
    sleep_ms(3000)  #200
    if radio.receive():
        if (radio.value != value_prev + 1 or not radio.key == key) and i > 2:
            print('ERROR')
            errors += 1
        else:
            successes +=1
        value_prev = radio.value
#         print('rssi:' + str(radio.rssi))
#     sleep_ms(400)
#     if radio.high_power == True:
#         radio.high_power = False
#     else:
#         radio.high_power = True
#     sleep_ms(3000)
    radio_tx_power = radio_tx_power + 1
    radio.tx_power = radio_tx_power
    print(str(i+1) + ': Radio power:' + str(radio.tx_power))
    sleep_ms(10000)
    radio.rfm69_reset()
        
error_rate = (errors / (errors + successes)) * 100
print('Error Rate: ' + str(error_rate) + '%')
