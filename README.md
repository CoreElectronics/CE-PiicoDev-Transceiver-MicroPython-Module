# PiicoDev® Radio MicroPython Module

<!-- TODO update link URL with CE SKU -->
<!-- TODO update link title -->
This is the firmware repo for the [Core Electronics PiicoDev® Radio](https://core-electronics.com.au/catalog/product/view/sku/CE08757)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

<!-- TODO update tutorial link with the device tinyurl eg. piico.dev/p1
See the [Quickstart Guide](https://piico.dev/p27)

<!-- TODO verify the tested-devices list
This module has been tested on:
 - Micro:bit v2
 - Raspberry Pi Pico
 - Raspberry Pi SBC
-->

## Initialisation

### `PiicoDev_Radio(bus=, freq=, sda=, scl=, address=0x35, id=, frequency=None)`
Parameter | Type | Range | Default | Description
--- | --- | --- | --- | ---
bus | int | 0,1 | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq | int | 100 to 1000000 | Device dependent | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda | Pin | Device Dependent | Device Dependent | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl | Pin | Device Dependent | Device Dependent | I2C SCL Pin. Implemented on Raspberry Pi Pico only
address | int | 0x35, 0x08 - 0x77 | 0x1A | Manually specify the address of the connected device. For when a software address is set on the device.
ID | List[int, int, int, int] | 1=ON, 0=OFF | [0,0,0,0] | Hardware switches change the device address - Abstracts the need for user to look up an address, simply input the switch positions. Alternatively, use `address` for explicit address.

## Properties

### `.temperature`

Discussion Points: seperate boards for 915 or 434 - this should make it easier to use

## Methods
###.`on()`

###.`off()`


Use this:
https://microbit-micropython.readthedocs.io/en/v1.0.1/radio.html

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
