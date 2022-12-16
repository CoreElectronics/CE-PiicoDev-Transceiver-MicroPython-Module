# PiicoDev® Transceiver MicroPython Module

This is the firmware repo for the [Core Electronics PiicoDev® Radio](https://core-electronics.com.au/catalog/product/view/sku/CE08757)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guide](https://piico.dev/p27)

<!-- TODO verify the tested-devices list
This module has been tested on:
 - Micro:bit v2
 - Raspberry Pi Pico
 - Raspberry Pi SBC
-->

## Overview

There are three message types that can be sent
| Type Number | Description
| ----------- | -----------
| 1           | key, value pair.  The key can be up to 55 characters and the value is an integer
| 2           | key, value pair.  The key can be up to 55 characters and the value is a float
| 3           | message of up to 59 characters


## Initialisation

### `PiicoDev_Transceiver(bus=, freq=, sda=, scl=, address=0x1A, id=, channel=0, radio_address=1, speed=2, radio_frequency=922, tx_power=20, suppress_warnings=False)`

| Parameter         | Type                     | Range             | Default                               | Description
| ----------------- | ------------------------ | ----------------- | ------------------------------------- | -----------
| bus               | int                      | 0,1               | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus. Ignored on Micro:bit.
| freq              | int                      | 100 to 1000000    | Device dependent                      | I2C Bus frequency (Hz). Ignored on Raspberry Pi.
| sda               | Pin                      | Device Dependent  | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only.
| scl               | Pin                      | Device Dependent  | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only.
| address           | int                      | 0x1A, 0x08 - 0x77 | 0x1A                                  | Manually specify the address of the connected device. For when a software address is set on the device.
| id                | List[int, int, int, int] | 1=ON, 0=OFF       | [0,0,0,0]                             | Hardware switches change the device address - Abstracts the need for user to look up an address, simply input the switch positions. Alternatively, use `address` for explicit address.
| channel           | int                      | 0 - 255           | 0                                     | Defines an arbitrary "channel" to which the radio is tuned. Messages will be sent via this channel and only messages received via this channel will shown.
| radio_adddress    | int                      | 0 - 127           | 1                                     | Used to filter incoming packets, keeping only those that match the address you set.
| speed             | int                      | 1, 2, 3           | 2                                     | See `.speed` property for more information.
| radio_frequency   | int                      | 915, 918, 922, 925, 228 | 922                             | See `.radio_frequency` property for more information.
| tx_power          | int                      | -2 to 20 dB       | 20                                    | See `.tx_power` property for more information.
| suppress_warnings | bool                     |                   | False                                 | If True, warnings will be suppressed

## Properties

### `.speed`
| Number | Baudrate (kbps) | Useage
| ------ | --------------- | ------
| 1      | 9.6             | Slower, longer range
| 2      | 115.2           | Balanced speed and range (default)
| 3      | 300             | Fastest, short range.

Example Usage:
``` Python
radio.speed = 1 # I want long range
print(radio.speed)
```

### `.radio_frequency`
Choose what frequency the radio will operate at. All radios must be tuned to the same frequency to communicate. Choose between 915, 918, 922(default), 925, 228.

Example Usage:
``` Python
radio.radio_frequency = 918 # I have interference at the default 922 MHz
print(radio.radio_frequency)
```

### `.tx_power`
Set the transmitter power

Example Usage:
``` Python
radio.tx_power = -2 # I don't want to interfeare with nearby devices
print(radio.tx_power)
```

## Methods

### `.off()`

Turns off the radio.

### `.on()`

Turns the radio on.

### `.rfm69_reset()`

Resets the radio.

### `.send(message, value, destination radio address)`

Sends a message string.

#### Examples

`radio.send('Hello')`

`radio.send('TempC', 25.0)`

`radio.send('Counter', 9)`

`radio.send('secret', radio_address=7)`

### `.receive()`

Checks for a new message.

``` Python
if radio.receive():
    if (radio.type == 3): 
        print(radio.message)
    else:
        print(radio.name, radio.value)
```

### Set or Get RFM69 Register Values

`value = radio.get_rfm69_register(0x29)`

`radio.set_rfm69_register(0x29, 221)`


## Payload

Note that when transmitting, no RSSI or from_radio_address from is sent, so:

Tx Position = Rx Position - 2


| Name                      | Rx Position | Bytes | Range        | Description
| ------------------------- | ----------- | ----- | ------------ | -----------
| rssi                      | 0           | 1     | 0 to 255     | RSSI (module negates the value)
| source_radio_address      | 1           | 1     | 0 to 127   | Source Radio Address
| type                      | 3           | 1     | 0 - 3        | Type of message (0: invalid, 1: key, int, 2: key, float, 3: message string)

If the type is 1 or 2:

| Name                      | Rx Position | Bytes | Range        | Description
| ------------------------- | ----------- | ----- | ------------ | -----------
| value                     | 4           | 4     |              | Value (int or float)
| length                    | 8           | 1     |              | Key length
| key                       | 9           | <=55  | 55 chars max | key

If the type is 3:

| Name                      | Rx Position | Bytes | Range        | Description
| ------------------------- | ----------- | ----- | ------------ | -----------
| length                    | 4           | 1     |              | Key length
| message                   | 5           | <=59  | 59 chars max | Message

## Smart Module I2C Registers

| Register Name     | Address   | Bytes  | Mode | Default Value    | Description
| ----------------- | --------- | ------ | ---- | ---------------- | -----------
| Device ID         | 0x01      | 2      | R    | 495              | I2C device ID
| Firmware Major    | 0x02      | 1      | R    | Varies           | Major firmware version
| Firmware Minor    | 0x03      | 1      | R    | Varies           | Minor firmware version
| I2C Address       | 0x84      | 1      | W    | 0xA1             | Set new I2C address
| LED               | 0x05/0x85 | 1      | R/W  | 1                | 0=OFF, 1=ON
| Tx Power          | 0x13/0x93 | 1      | R/W  |                  | -2 to +20 dBm
| RFM69 Radio State | 0x14/0x94 | 1      | R/W  | 0                | 0=OFF, 1=ON
| RFM69 Node ID     | 0x15/0x95 | 2      | R/W  | 1                | 
| RFM69 Network ID  | 0x16/0x96 | 1      | R/W  | 0                | 
| RFM69 To Node ID  | 0x17/0x97 | 2      | R/W  | 0                | 
| RFM69 Reg         | 0x98      | 1      | W    | N/A              | To read or write to a register in the RFM69, write the address of interest to this register then read or write the value to _RFM69 Value_ Register
| RFM69 Value       | 0x19/0x99 | 1      | R/W  | N/A              | To read or write to a register in the RFM69, write the address of interest to _RFM69 Reg_ Register then read or write the value this register
| RFM69 Reset       | 0xA0      | 1      | W    | 0                | Set to 1 to reset
| Payload Length    | 0x21/0xA1 | 1      | R/W  | N/A              | To send a message, write to the _Payload_ register, then write the length to this register to trigger sending of the message over the air. Read this register to check for a new message.
| Payload           | 0x22/0xA2 | 26 Max | R/W  | N/A              | To send a message, write the payload to this register, then write the length to the _Payload Length_ register to trigger sending of the message over the air. Read this register to check the contents of a new message.
| Payload New       | 0x23      | 1      | R    | 0                | A 1 indicates a new message has been received
| Payload Go        | 0xA4      | 1      | W    | 0                | To send a message, write to the length, then payload then set this to 1 to send the message
| Transceiver Ready | 0x25      | 1      | R    | 0                | Wait for the tranceiver to be ready before sending the next command

This library has been inspired by the [Micro:bit Radio library](https://microbit-micropython.readthedocs.io/en/v1.0.1/radio.html).

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*

Outstanding Issues:
Tx Power doesn't seem to make any difference
Now that we are using the radio's built-in addressing scheme, need to make it so that we send the from 