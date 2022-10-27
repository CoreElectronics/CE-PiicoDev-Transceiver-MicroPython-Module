from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Potentiometer import PiicoDev_Potentiometer
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

while True:
    firmware = radio.firmware
#     print('ID:             ' + str(radio.whoami))
#     print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
#     print('Encryption:     ' + str(radio.encryption))
#     print('Encryption Key: ' + str(radio.encryption_key))
#     print('High Power:     ' + str(radio.high_power))
#     print('Node ID:        ' + str(radio.rfm69_node_id))
#     print('Network ID:     ' + str(radio.rfm69_network_id))
#     print('To Node ID:     ' + str(radio.rfm69_to_node_id))
    radio.led = 1
    sleep_ms(50)
#     print('value:'+str(value))
#    radio.send('!hello world', value=0)
#     print('hello world sent')
    sleep_ms(50)
    incoming_datagram = radio.receive()
    if incoming_datagram != 0:
#         print('incoming_datagram' + str(incoming_datagram))
        print('value: ' + hex(incoming_datagram[0]))
    sleep_ms(100)
