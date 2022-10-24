from PiicoDev_Radio import PiicoDev_Radio
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Radio()   # Initialise the Radio module

while True:
    #radio.on()
    firmware = radio.firmware
    print('ID:             ' + str(radio.whoami))
    print('Firmware:       ' + str(firmware[0]) + '.' + str(firmware[1]))
    print('Encryption:     ' + str(radio.encryption))
    print('Encryption Key: ' + str(radio.encryption_key))
    print('High Power:     ' + str(radio.high_power))
    print('Node ID:        ' + str(radio.rfm69_node_id))
    print('Network ID:     ' + str(radio.rfm69_network_id))
    print('To Node ID:     ' + str(radio.rfm69_to_node_id))
    radio.led = 1
    sleep_ms(50)
    radio.message = '!hello world'
    print('hello world sent')
    sleep_ms(1000)
    received_message = radio.message
    print('Received Message:' + str(received_message))
    #radio.off()
    sleep_ms(2000)