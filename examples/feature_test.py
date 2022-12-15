from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

ID = [0,0,0,0]
# ID = [1,0,0,0]
# ID = [0,1,0,0]
# ID = [0,0,1,0]
# ID = [0,0,0,1]
SPEED = 1
TX_POWER = 20
MESSAGE = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVW'
KEY = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRS'
DESTINATION_ADDRESS = 2

# radio = PiicoDev_Transceiver(address=0x33)
radio = PiicoDev_Transceiver(id=ID, channel=0, radio_address=1, speed=SPEED, radio_frequency=922, tx_power=TX_POWER, suppress_warnings=False, debug=False)

def test_led():
    print('Flashing LED 3 times...')
    for x in range(3):
        radio.led = False
        print("LED ON: " + str(radio.led))
        sleep_ms(500)
        radio.led = True
        print("LED ON: " + str(radio.led))
        sleep_ms(500)

def test_off_and_on():
    radio.send('About to turn the radio OFF', address=DESTINATION_ADDRESS)
    print('About to turn the radio OFF')
    radio.off()
    radio.send('The radio should be OFF', address=DESTINATION_ADDRESS)
    print('The radio should be OFF')
    sleep_ms(100)
    radio.send('The radio should still be OFF', address=DESTINATION_ADDRESS)
    print('The radio should still be OFF')
    sleep_ms(100)
    radio.on()
    radio.send('The radio should now be back ON', address=DESTINATION_ADDRESS)
    print('The radio should now be back ON')

def test_send_message():
    radio.send(MESSAGE, address=DESTINATION_ADDRESS)
    sleep_ms(300) # Compatible with 9600 baud
    if radio.receive():
        print('Source Radio Address:'+str(radio.source_radio_address)+' Type:'+str(radio.type)+' Message:'+str(radio.message) + " RSSI:" + str(radio.rssi))

# radio.setI2Caddr(0x33)
firmware = radio.firmware
print('       Firmware: ' + str(firmware[0]) + '.' + str(firmware[1]))
print('       Who I Am: ' + str(radio.whoami))
print('          Speed: ' + str(radio.speed))
print('Radio Frequency: ' + str(radio.radio_frequency))
print('       Tx Power: ' + str(radio.tx_power))

radio.led = True

test_send_message()
#test_led()
test_off_and_on()

while True:

#print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.value) + ':' + str(radio.key) + " RSSI:" + str(radio.rssi))
   sleep_ms(1000)
