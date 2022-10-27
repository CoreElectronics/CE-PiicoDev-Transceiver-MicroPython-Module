# 2022-08-10 https://github.com/bbcmicrobit/micropython/tree/v1.0.1
# Peter Johnston at Core Electronics
# 2022-10-19: Initial release

from PiicoDev_Unified import *
import radio_config
from struct import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_BASE_ADDRESS                  = 0xA1
_DEVICE_ID                     = 495

_REG_WHOAMI                    = 0x01
_REG_FIRM_MAJ                  = 0x02
_REG_FIRM_MIN                  = 0x03
_REG_I2C_ADDRESS               = 0x04
_REG_LED                       = 0x05
_REG_ENCRYPTION                = 0x11
_REG_ENCRYPTION_KEY            = 0x12
_REG_HIGH_POWER                = 0x13
_REG_RFM69_RADIO_STATE         = 0x14
_REG_RFM69_NODE_ID             = 0x15
_REG_RFM69_NETWORK_ID          = 0x16
_REG_RFM69_TO_NODE_ID          = 0x17
_REG_RFM69_REG                 = 0x18
_REG_RFM69_VALUE               = 0x19
_REG_PAYLOAD_LENGTH            = 0x21
_REG_PAYLOAD                   = 0x22
_REG_PAYLOAD_NEW               = 0x23
_REG_PAYLOAD_GO                = 0x24

DEBUG = True

def _set_bit(x, n):
    return x | (1 << n)

def debug(text):
    if DEBUG:
        print(text)

class PiicoDev_Radio(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_BASE_ADDRESS, id=None, radio_address=radio_config.radio_address, channel=radio_config.channel, suppress_warnings=False):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl, suppress_warnings=suppress_warnings)
        self._address = address
        if type(id) is list and not all(v == 0 for v in id): # preference using the ID argument. ignore id if all elements zero
            assert max(id) <= 1 and min(id) >= 0 and len(id) == 4, "id must be a list of 1/0, length=4"
            self._address=8+id[0]+2*id[1]+4*id[2]+8*id[3] # select address from pool
        else: self._address = address # accept an integer
        self.radio_address = radio_address
        self.channel = channel
        self.destination_radio_address = radio_config.destination_radio_address
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
        
    def send_payload(self, payload):
#         print('payload length ' + str(len(payload)))
        self._write_int(_set_bit(_REG_PAYLOAD_LENGTH, 7), len(payload))
        sleep_ms(10)
        self._write(_set_bit(_REG_PAYLOAD, 7), payload)
        sleep_ms(10)
        #print('---')
        self._write_int(_set_bit(_REG_PAYLOAD_GO, 7), 1)
        
    def receive_payload(self):
        payload = 0
#         print('receive payload')
        if self._payload_new == 1:
            payload_length = self._read_int(_REG_PAYLOAD_LENGTH)
#             print('RECEIVED_PAYLOAD_LENGTH:' + str(payload_length))
            payload = self._read(_REG_PAYLOAD, length=payload_length)
#             print('RECEIVED PAYLOAD:' + str(payload))
        return payload
    
    def on(self):
        self._on = 1
        
    def off(self):
        self._off = 1
    
    @property
    def encryption(self):
        return self._read_int(_REG_ENCRYPTION)
    
    @encryption.setter
    def encryption(self, value):
        self._write_int(_set_bit(_REG_ENCRYPTION, 7), value)
        
    @property
    def encryption_key(self):
        return self._read(_REG_ENCRYPTION_KEY)
    
    @encryption_key.setter
    def encryption_key(self, value):
        self._write_int(_set_bit(_REG_ENCRYPTION_KEY, 7), value)
        
    @property
    def high_power(self):
        return self._read_int(_REG_HIGH_POWER)
    
    @high_power.setter
    def high_power(self, value):
        self._write_int(_set_bit(_REG_HIGH_POWER, 7), value)
    
    @property
    def rfm69_network_id(self):
        return self._read_int(_REG_RFM69_NETWORK_ID)
    
    @rfm69_network_id.setter
    def rfm69_network_id(self, value):
        print("channel setter called")
        self._write_int(_set_bit(_REG_RFM69_NETWORK_ID, 7), value)
    
    @property
    def rfm69_node_id(self):
        return self._read_int(_REG_RFM69_NODE_ID)
    
    @rfm69_node_id.setter
    def rfm69_node_id(self, value):
        self._write_int(_set_bit(_REG_RFM69_NODE_ID, 7), value)
        
    @property
    def rfm69_to_node_id(self):
        return self._read_int(_REG_RFM69_TO_NODE_ID)
    
    @rfm69_to_node_id.setter
    def rfm69_to_node_id(self, value):
        debug("Setting destination radio address to " + str(value) + ".")
        self._write_int(_set_bit(_REG_RFM69_TO_NODE_ID, 7), value)
    
    @property
    def payload_length(self):
        return 0
    
    @payload_length.setter
    def payload_length(self, value):
        debug("Setting message length" + str(value) + ".")
        self._write_int(_set_bit(_REG_PAYLOAD_LENGTH, 7), value)
        
    @property
    def _payload_new(self):
        return self._read_int(_REG_PAYLOAD_NEW)
    
    def receive(self):
        data = 0
        payload = self.receive_payload()
        if payload != 0:
#             print('--------------------------------------')
            data = unpack('B', bytes(payload))
#            data = unpack('BBfB13s', bytes(payload))
#             print('received:' + str(data))
        #message_string = str(self.receive_payload(), 'utf8')
        #message_string = str(self.receive_bytes())
        return data
    
    def send(self, message_string, value=0.0, destination_radio_address=0):
        #s = Struct()
        #print('self.radio_address:' + str(self.radio_address))
        #print('destination_radio_address:' + str(destination_radio_address))
        #print('value:' + str(value))
        #print('message_length' + str(len(message_string)))
        #print('message_string:' + str(message_string))
        data = pack('B', int(value))
#         data = pack('BBBB13s', self.radio_address, destination_radio_address, int(value), len(message_string), bytes(message_string, 'utf8'))
#         print('sending message')
#         print(data)
        #self.send_payload(bytes(message_string, 'utf8'))
        self.send_payload(data)
    
    @property
    def _on(self):
        """Checks the radio state"""
        self._read_int(_REG_RFM69_RADIO_STATE, 1)
    
    @_on.setter
    def _on(self, val):
        """Turns the radio on"""
        print('Turning radio on!')
        self._write_int(_set_bit(_REG_RFM69_RADIO_STATE, 7), 1)
    
    @property
    def _off(self):
        """Checks the radio state"""
        print('Turning radio off')
        self._read_int(_REG_RFM69_RADIO_STATE, 0)
    
    @_off.setter
    def _off(self, val):
        """Turns the radio off"""
        self._write_int(_set_bit(_REG_RFM69_RADIO_STATE, 7), 0)
    
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
