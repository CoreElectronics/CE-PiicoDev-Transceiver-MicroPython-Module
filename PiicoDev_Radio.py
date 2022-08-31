# 2022-08-10 https://github.com/bbcmicrobit/micropython/tree/v1.0.1
# Peter Johnston at Core Electronics
# 2022-08-24: Initial release

from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_BASE_ADDRESS = 0xA1
_DEVICE_ID    = 495

_REG_STATUS       = 0x01
_REG_FIRM_MAJ     = 0x02
_REG_FIRM_MIN     = 0x03
_REG_I2C_ADDRESS  = 0x04
_REG_LED          = 0x05
_REG_RADIO_ON     = 0x06
_REG_WHOAMI       = 0x11
_REG_MESSAGE      = 0x21

def _set_bit(x, n):
    return x | (1 << n)

class PiicoDev_Radio(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_BASE_ADDRESS, id=None):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self._address = address
        if type(id) is list and not all(v == 0 for v in id): # preference using the ID argument. ignore id if all elements zero
            assert max(id) <= 1 and min(id) >= 0 and len(id) == 4, "id must be a list of 1/0, length=4"
            self._address=8+id[0]+2*id[1]+4*id[2]+8*id[3] # select address from pool
        else: self._address = address # accept an integer
        try:
            if self.whoami != _DEVICE_ID:
                print("* Incorrect device found at address {}".format(address))   
        except:
            print("* Couldn't find a device - check switches and wiring")
    
    def _read(self, register, length=1):
        try:
            return self.i2c.readfrom_mem(self.address, register, length)
        except:
            print(i2c_err_str.format(self.address))
            return None

    def _write(self, register, data):
        try:
            self.i2c.writeto_mem(self.address, register, data)
        except:
            print(i2c_err_str.format(self.address))

    def _read_int(self, register, length=1):
        data = self._read(register, length)
        if data is None:
            return None
        else:
            return int.from_bytes(data, 'big')

    def _write_int(self, register, integer, length=1):
        self._write(register, int.to_bytes(integer, length, 'big'))
        
    def send_bytes(self, message):
        self._write(_set_bit(_REG_MESSAGE, 7), message)
        
    def receive_bytes(self):
        message = self._read(_REG_MESSAGE)
        return message
    
    def on(self):
        self._on = 1
        
    def off(self):
        self._off = 1
    
    @property
    def message(self):
        message_string = str(self.receive_bytes(), 'utf8')
        return message_string
    
    @message.setter
    def message(self, message_string):
        self.send_bytes(bytes(message_string, 'utf8'))
    
    @property
    def _on(self):
        """Checks the radio state"""
        self._read_int(_REG_RADIO_ON, 1)
    
    @_on.setter
    def _on(self, val):
        """Turns the radio on"""
        print('Turning radio on')
        self._write_int(_set_bit(_REG_RADIO_ON, 7), 1)
    
    @property
    def _off(self):
        """Checks the radio state"""
        print('Turning radio off')
        self._read_int(_REG_RADIO_ON, 0)
    
    @_off.setter
    def _off(self, val):
        """Turns the radio off"""
        self._write_int(_set_bit(_REG_RADIO_ON, 7), 0)
    
    @property
    def address(self):
        """Returns the currently configured 7-bit I2C address"""
        return self._address

    @property
    def led(self):
        """Returns the state onboard "Power" LED. `True` / `False`"""
        return bool(self._read_int(_REG_LED))
    
    @led.setter
    def led(self, x):
        """control the state onboard "Power" LED. accepts `True` / `False`"""
        self._write_int(_set_bit(_REG_LED, 7), int(x))

    @property
    def whoami(self):
        """returns the device identifier"""
        return self._read_int(_REG_WHOAMI, 2)
    
    @property
    def firmware(self):
        """Returns the firmware version"""
        v=[0,0]
        v[1]=self._read_int(_REG_FIRM_MAJ)
        v[0]=self._read_int(_REG_FIRM_MIN)
        return (v[1],v[0])
    
    def setI2Caddr(self, newAddr):
        x=int(newAddr)
        assert 8 <= x <= 0x77, 'address must be >=0x08 and <=0x77'
        self._write_int(_REG_I2C_ADDRESS, x)
        self._address = x
        sleep_ms(5)
        return 0
