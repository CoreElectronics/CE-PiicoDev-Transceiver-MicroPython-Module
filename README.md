# PiicoDev® Radio MicroPython Module

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

![Overview](docs/overview.svg "Overview")

## Initialisation

### `PiicoDev_Radio(bus=, freq=, sda=, scl=, address=0x1A, id=, frequency=None, radio_address=0, channel=0, queue=3)`

| Parameter      | Type                     | Range             | Default                               | Description
| -------------- | ------------------------ | ----------------- | ------------------------------------- | -----------
| bus            | int                      | 0,1               | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus. Ignored on Micro:bit.
| freq           | int                      | 100 to 1000000    | Device dependent                      | I2C Bus frequency (Hz). Ignored on Raspberry Pi.
| sda            | Pin                      | Device Dependent  | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only.
| scl            | Pin                      | Device Dependent  | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only.
| address        | int                      | 0x1A, 0x08 - 0x77 | 0x1A                                  | Manually specify the address of the connected device. For when a software address is set on the device.
| id             | List[int, int, int, int] | 1=ON, 0=OFF       | [0,0,0,0]                             | Hardware switches change the device address - Abstracts the need for user to look up an address, simply input the switch positions. Alternatively, use `address` for explicit address.
| radio_adddress | int                      | 0 - 255           | 0                                     | See the `.radio_address` property for more information
| channel        | int                      | 0 - 255           | 0                                     | See the `.channel` property for more information
| queue          | int                      | 0 - 255           | 3                                     | See the `.queue` property for more information


## Properties

### `.radio_address`

(default=0) is an arbitrary name, expressed as an integer value from 0 to 255 (inclusive), that's used to filter incoming packets, keeping only those that match the address you set.

### `.channel`

(default=0) can be an integer value from 0 to 255 (inclusive) that defines an arbitrary "channel" to which the radio is tuned. Messages will be sent via this channel and only messages received via this channel will be put onto the incoming message queue.  If the channel is set to 0, all channels will be received and messages sent will be received by all radios regardless of what channel they are set to.

### `.queue`

(default=3) specifies the number of messages that can be stored on the incoming message queue. If there are no spaces left on the queue for incoming messages, then the incoming message is dropped.

### `.power`

(default=6) is an integer value from 0 to 7 (inclusive) to indicate the strength of signal used when broadcasting a message. The higher the value the stronger the signal, but the more power is consumed by the device. The numbering translates to positions in the following list of dBm (decibel milliwatt) values: -30, -20, -16, -12, -8, -4, 0, 4.

### `.data_rate`

(default=radio.RATE_1MBIT) indicates the speed at which data throughput takes place. Can be one of the following contants defined in the ``radio`` module : `RATE_250KBIT`, `RATE_1MBIT` or `RATE_2MBIT`.

## Methods

### `.on()`

Turns the radio on.

### `.off()`

Turns off the radio.

### `.send(message)`

Sends a message string. This is the equivalent of send_bytes(bytes(message, 'utf8'))

### `.receive()`

### `.write_reg(reg_address, value)`

Writes to a specific register in the the RFM69 

Works in exactly the same way as receive_bytes but returns whatever was sent.
Currently, it’s equivalent to str(receive_bytes(), 'utf8').



## Smart Module I2C Registers

| Register Name     | Address   | Bytes  | Mode | Default Value    | Description
| ----------------- | --------- | ------ | ---- | ---------------- | -----------
| Device ID         | 0x01      | 2      | R    | 495              | I2C device ID
| Firmware Major    | 0x02      | 1      | R    | Varies           | Major firmware version
| Firmware Minor    | 0x03      | 1      | R    | Varies           | Minor firmware version
| I2C Address       | 0x84      | 1      | W    | 0xA1             | Set new I2C address
| LED               | 0x05/0x85 | 1      | R/W  | 1                | 0=OFF, 1=ON
| Encryption        | 0x11/0x91 | 1      | R/W  | 0                | 0=OFF, 1=ON
| Encryption Key    | 0x12/0x92 | 2      | R/W  | PiicoDev---Radio | Must be exactly 16 characters on all nodes
| High Power        | 0x13/0x93 | 1      | R/W  | 0                | 0=OFF, 1=ON
| RFM69 Radio State | 0x14/0x94 | 1      | R/W  | 0                | 0=OFF, 1=ON
| RFM69 Node ID     | 0x15/0x95 | 1      | R/W  | 1                | Do not change, addressing handled by the MicroPython driver
| RFM69 Network ID  | 0x16/0x96 | 1      | R/W  | 0                | Do not change, addressing handled by the MicroPython driver
| RFM69 To Node ID  | 0x17/0x97 | 1      | R/W  | 0                | Do not change, addressing handled by the MicroPython driver
| RFM69 Reg         | 0x98      | 1      | W    | N/A              | To read or write to a register in the RFM69, write the address of interest to this register then read or write the value to _RFM69 Value_ Register
| RFM69 Value       | 0x19/0x99 | 1      | R/W  | N/A              | To read or write to a register in the RFM69, write the address of interest to _RFM69 Reg_ Register then read or write the value this register
| Payload Length    | 0x21/0xA1 | 1      | R/W  | N/A              | To send a message, write to the _Payload_ register, then write the length to this register to trigger sending of the message over the air. Read this register to check for a new message.
| Payload           | 0x22/0xA2 | 26 Max | R/W  | N/A              | To send a message, write the payload to this register, then write the length to the _Payload Length_ register to trigger sending of the message over the air. Read this register to check the contents of a new message.
| Payload Go        | 0xA3      | 1      | W    | 0                | To send a message, write to the length, then payload then set this to 1 to send the message

This library has been inspired by the [Micro:bit Radio library](https://microbit-micropython.readthedocs.io/en/v1.0.1/radio.html).

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
