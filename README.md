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

## Initialisation

### `PiicoDev_Radio(bus=, freq=, sda=, scl=, address=0x1A, id=, frequency=None)`
Parameter | Type | Range | Default | Description
--- | --- | --- | --- | ---
bus | int | 0,1 | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq | int | 100 to 1000000 | Device dependent | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda | Pin | Device Dependent | Device Dependent | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl | Pin | Device Dependent | Device Dependent | I2C SCL Pin. Implemented on Raspberry Pi Pico only
address | int | 0x1A, 0x08 - 0x77 | 0x1A | Manually specify the address of the connected device. For when a software address is set on the device.
id | List[int, int, int, int] | 1=ON, 0=OFF | [0,0,0,0] | Hardware switches change the device address - Abstracts the need for user to look up an address, simply input the switch positions. Alternatively, use `address` for explicit address.

## Properties

### `.length`

(default=32) defines the maximum length, in bytes, of a message sent via the radio. It can be up to 251 bytes long (254 - 3 bytes for S0, LENGTH and S1 preamble).

### `.queue`

(default=3) specifies the number of messages that can be stored on the incoming message queue. If there are no spaces left on the queue for incoming messages, then the incoming message is dropped.

### `.channel`

(default=7) can be an integer value from 0 to 83 (inclusive) that defines an arbitrary "channel" to which the radio is tuned. Messages will be sent via this channel and only messages received via this channel will be put onto the incoming message queue. Each step is 1MHz wide, based at 2400MHz.

### `.power`
(default=6) is an integer value from 0 to 7 (inclusive) to indicate the strength of signal used when broadcasting a message. The higher the value the stronger the signal, but the more power is consumed by the device. The numbering translates to positions in the following list of dBm (decibel milliwatt) values: -30, -20, -16, -12, -8, -4, 0, 4.

### `.address`
(default=0x75626974) is an arbitrary name, expressed as a 32-bit address, that's used to filter incoming packets at the hardware level, keeping only those that match the address you set. The default used by other micro:bit related platforms is the default setting used here.

### `.group`
(default=0) is an 8-bit value (0-255) used with the `address` when filtering messages. Conceptually, "address" is like a house/office address and "group" is like the person at that address to which you want to send your message.

### `.data_rate`
(default=radio.RATE_1MBIT) indicates the speed at which data throughput takes place. Can be one of the following contants defined in the ``radio`` module : `RATE_250KBIT`, `RATE_1MBIT` or `RATE_2MBIT`.

## Methods
### `.on()`

### `.off()`

### `.send(message)`
Sends a message string. This is the equivalent of send_bytes(bytes(message, 'utf8'))

### `.receive()`
Works in exactly the same way as receive_bytes but returns whatever was sent.
Currently, it’s equivalent to str(receive_bytes(), 'utf8').

This library has been inspired by the [Micro:bit Radio library](https://microbit-micropython.readthedocs.io/en/v1.0.1/radio.html).

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
