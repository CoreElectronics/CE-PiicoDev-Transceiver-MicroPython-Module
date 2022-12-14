from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio(radio_address=1, channel=0)

firmware = radio.firmware
print('ID:             ' + str(radio.whoami))
print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
print('Tx Power:       ' + str(int(radio.tx_power)))
print('Radio Address   ' + str(radio.radio_address))
print('Channel:        ' + str(radio.channel))

radio.tx_power = 20
radio.speed = 2

while True:
    if radio.receive():
#         print(" RSSI:" + str(radio.rssi))
#         print("Source Radio Address:" + str(radio.source_radio_address))
#         print("Message Type:" + str(radio.type))
#         print("Value:" + str(radio.value))
#         print("Key:" + str(radio.key))
        print(str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.value) + ':' + str(radio.key) + " RSSI:" + str(radio.rssi))
        radio.send(radio.key, radio.value)
    sleep_ms(5)