from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver(radio_address=2, speed=2, channel=0)

firmware = radio.firmware
print('ID:             ' + str(radio.whoami))
print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
print('Tx Power:       ' + str(int(radio.tx_power)))
print('Radio Address   ' + str(radio.radio_address))
print('Channel:        ' + str(radio.channel))

while True:
    if radio.receive():
        if radio.type == 3:
            print('Source Address' + str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.message) + " RSSI:" + str(radio.rssi))
            radio.send(radio.message, address=radio.source_radio_address)
        else:
            print('Source Address' + str(radio.source_radio_address)+':'+str(radio.type)+':'+str(radio.value) + ':' + str(radio.key) + " RSSI:" + str(radio.rssi))
            radio.send(radio.key, radio.value, address=radio.source_radio_address)
    sleep_ms(5)