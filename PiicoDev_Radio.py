# 2022-08-10 https://github.com/bbcmicrobit/micropython/tree/v1.0.1
# Peter Johnston at Core Electronics
# 2022-10-19: Initial release

from PiicoDev_Unified import *
from struct import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_BASE_ADDRESS          = 0x1A
_DEVICE_ID             = 495

_REG_WHOAMI            = 0x01
_REG_FIRM_MAJ          = 0x02
_REG_FIRM_MIN          = 0x03
_REG_I2C_ADDRESS       = 0x04
_REG_LED               = 0x05
_REG_TX_POWER          = 0x13
_REG_RFM69_RADIO_STATE = 0x14
_REG_RFM69_NODE_ID     = 0x15
_REG_RFM69_NETWORK_ID  = 0x16
_REG_RFM69_TO_NODE_ID  = 0x17
_REG_RFM69_REG         = 0x18
_REG_RFM69_VALUE       = 0x19
_REG_RFM69_RESET       = 0x20
_REG_PAYLOAD_LENGTH    = 0x21
_REG_PAYLOAD           = 0x22
_REG_PAYLOAD_NEW       = 0x23
_REG_PAYLOAD_GO        = 0x24
_REG_TRANSCEIVER_READY = 0x25

_RFM69_REG_BITRATEMSB  = 0x03
_RFM69_REG_BITRATELSB  = 0x04
_RFM69_REG_FRFMSB      = 0x07
_RFM69_REG_FRFMID      = 0x08
_RFM69_REG_FRFLSB      = 0x09

_MAXIMUM_PAYLOAD_LENGTH = 61 # The Low Power Labs Arduino library is limited to 65 bytes total payload including a 4 header bytes
_MAXIMUM_I2C_SIZE = 32 #For ATmega328 based Arduinos, the I2C buffer is limited to 32 bytes

def tempdebug(text):
    print(str(ticks_ms() - start_time) + ':' + str(value))

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def _set_bit(x, n):
    return x | (1 << n)

class PiicoDev_Radio(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_BASE_ADDRESS, id=None, channel=0, radio_address=1, speed=2, radio_frequency=922, tx_power=20, suppress_warnings=False, debug=False):
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
        self.debug=debug
        if radio_address < 0:
            radio_address = 0
        if radio_address > 127: # Only 7 bits seem to go over the air so any address higher than 127 gives an incorrect source address
            radio_address = 127
        self._write_int(_REG_RFM69_NODE_ID, radio_address, 2)
        self._write_int(_REG_RFM69_NETWORK_ID, channel)
#         self.destination_radio_address = radio_config.destination_radio_address
        self.rssi = 0
        self.type = 0
        self.message = ''
        self.key = ''
        self.value = None
        self.source_radio_address = 0
        self.radio_frequency = radio_frequency
        self.speed = speed
        self.tx_power = tx_power
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
            self.i2c.writeto_mem(self.address, _set_bit(register, 7), data)
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
         # if the payload is too long, truncate it
        payload_list = [payload[i:i+_MAXIMUM_I2C_SIZE-1] for i in range(0, len(payload), _MAXIMUM_I2C_SIZE-1)] # Split the bytes into a list
        self._write_int(_REG_PAYLOAD_LENGTH, len(payload))
        sleep_ms(5)
        for i in range(len(payload_list)):
            self._write(_REG_PAYLOAD, payload_list[i])
            sleep_ms(5) #was 12
        self._write_int(_REG_PAYLOAD_GO, 1)
        
    def receive_payload(self):
        payload_length = 0
        payload = bytes(0)
        if self._payload_new == 1:
            if self.debug:
                sleep_ms(100) # for debug mode
                print('delay')
            payload_length = self._read_int(_REG_PAYLOAD_LENGTH) + 3 # _MAXIMUM_PAYLOAD_LENGTH + RSSI + source_radio_address
            unprocessed_payload_length = payload_length
            sleep_ms(5)
            number_of_chunks = int(truncate(payload_length / _MAXIMUM_I2C_SIZE))+1
            for i in range(number_of_chunks):
                chunk_length = _MAXIMUM_I2C_SIZE
                if unprocessed_payload_length < 32:
                    chunk_length = unprocessed_payload_length
                payload = payload + self._read(_REG_PAYLOAD, length=chunk_length)
                unprocessed_payload_length -= _MAXIMUM_I2C_SIZE
                sleep_ms(5)
            payload = payload[:payload_length]
        return payload_length, payload
    
    def on(self):
        self._on = 1
        
    def off(self):
        self._off = 1
        
    @property
    def tx_power(self):
        while self.transceiver_ready == False:
            sleep_ms(10)
        value = unpack('b', self._read(_REG_TX_POWER))
        return value[0]
    
    @tx_power.setter
    def tx_power(self, value):
        if value < -2:
            value = -2
        if value > 20:
            value = 20
        while self.transceiver_ready == False:
            sleep_ms(10)
        self._write(_REG_TX_POWER, pack('b',value))
    
    @property
    def channel(self):
        """ There is no setter because we only want to set when initialising because changing this will trigger a re-initialise in the arduino"""
        return self._read_int(_REG_RFM69_NETWORK_ID)
    
    @property
    def radio_address(self):
        """ There is no setter because we only want to set when initialising because changing this will trigger a re-initialise in the arduino"""
        return self._read_int(_REG_RFM69_NODE_ID, 2)
        print("Node ID Called")
        
    @property
    def destination_radio_address(self):
        return self._read_int(_REG_RFM69_TO_NODE_ID, 2)
    
    @destination_radio_address.setter
    def destination_radio_address(self, value):
        self._write_int(_REG_RFM69_TO_NODE_ID, value, 2)
    
    def rfm69_reset(self):
        debug("Resetting RFM69")
        self._write_int(_REG_RFM69_RESET, 1)
    
    @property
    def payload_length(self):
        return 0
    
    @payload_length.setter
    def payload_length(self, value):
        self._write_int(_REG_PAYLOAD_LENGTH, value)
        
    @property
    def _payload_new(self):
        return self._read_int(_REG_PAYLOAD_NEW)
    
    def receive(self):
        payload_length, payload = self.receive_payload()
        if payload_length != 0:
            payload_bytes = bytes(payload)
            self.rssi = -int.from_bytes(payload_bytes[:1], 'big')
            self.source_radio_address = int.from_bytes(payload_bytes[1:3], 'big')
            self.type = int.from_bytes(payload_bytes[3:4], 'big')
            try:
                if self.type == 1:
                    self.key = str(payload_bytes[9:], 'utf8')
                    self.value = unpack('>i', (payload_bytes[4:8]))[0]
                if self.type == 2:
                    self.key = str(payload_bytes[9:], 'utf8')
                    self.value = unpack('>f', (payload_bytes[4:8]))[0]
                if self.type == 3:
                    self.message = str(payload_bytes[4:], 'utf8')
            except:
                print('* error parsing payload')
            return True
        return False
    
    def send(self, message_string, value=None, address=0):
        self.destination_radio_address = address
        if isinstance(value, int):
            type = 1
            message_string = message_string[:(_MAXIMUM_PAYLOAD_LENGTH-6)]
            format_characters = '>BiB' + str(len(message_string)) + 's'
            data = pack(format_characters, type, value, len(message_string), bytes(message_string, 'utf8'))
        if isinstance(value, float):
            type = 2
            message_string = message_string[:(_MAXIMUM_PAYLOAD_LENGTH-6)]
            format_characters = '>BfB' + str(len(message_string)) + 's'
            data = pack(format_characters, type, value, len(message_string), bytes(message_string, 'utf8'))
        if value is None:
            type = 3
            message_string = message_string[:(_MAXIMUM_PAYLOAD_LENGTH-2)]
            format_characters = '>BB' + str(len(message_string)) + 's'
            data = pack(format_characters, type, len(message_string), bytes(message_string, 'utf8'))
        self.send_payload(data)
        
    def send_byte(self, value):
        data = pack('B', value)
        self.send_payload(data)
        
    def receive_byte(self):
        data = 0
        payload = self.receive_payload()
        if payload != 0:
           data = int.from_bytes(payload,"big")
        return data
    
    def get_rfm69_register(self, register):
        self._write_int(_REG_RFM69_REG, register)
        return self._read_int(_REG_RFM69_VALUE)
        
    def set_rfm69_register(self, register, value):
        self._write_int(_REG_RFM69_REG, register)
        self._write_int(_REG_RFM69_VALUE, value)
    
    @property
    def radio_frequency(self):
        return self._radio_frequency
    
    @radio_frequency.setter
    def radio_frequency(self, frequency):
        while self.transceiver_ready == False:
            sleep_ms(10)
        if frequency == 915:
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMSB,0xE4)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMID,0xC0)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFLSB,0x00)
            sleep_ms(5)
            self._radio_frequency = 915
            print('frequency set to 915')
        elif frequency == 918:
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMSB,0xE5)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMID,0x80)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFLSB,0x00)
            sleep_ms(5)
            self._radio_frequency = 918
            print('frequency set to 918')
        elif frequency == 922:
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMSB,0xE6)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMID,0x80)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFLSB,0x00)
            sleep_ms(5)
            self._radio_frequency = 922
            print('frequency set to 922')
        elif frequency == 925:
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMSB,0xE7)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMID,0x40)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFLSB,0x00)
            sleep_ms(5)
            self._radio_frequency = 925
            print('frequency set to 925')
        elif frequency == 928:
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMSB,0xE8)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFMID,0x00)
            sleep_ms(5)
            self.set_rfm69_register(_RFM69_REG_FRFLSB,0x00)
            sleep_ms(5)
            self._radio_frequency = 928
            print('frequency set to 928')
        else:
            print(' * frequency not supported')
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        if speed == 1: # 9600
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATEMSB,0x0D)
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATELSB,0x05)
            sleep_ms(10)
            self._speed = 1
        elif speed == 2: # 115200
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATEMSB,0x01)
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATELSB,0x16)
            sleep_ms(10)
            self._speed = 2
        elif speed == 3: # 300000
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATEMSB,0x00)
            sleep_ms(10)
            self.set_rfm69_register(_RFM69_REG_BITRATELSB,0x6B)
            sleep_ms(10)
            self._speed = 3
        else:
            print('* speed not valid')
    
    @property
    def _on(self):
        """Checks the radio state"""
        self._read_int(_REG_RFM69_RADIO_STATE, 1)
    
    @_on.setter
    def _on(self, val):
        """Turns the radio on"""
        print('Turning radio on!')
        self._write_int(_REG_RFM69_RADIO_STATE, 1)
    
    @property
    def _off(self):
        """Checks the radio state"""
        self._read_int(_REG_RFM69_RADIO_STATE, 0)
    
    @_off.setter
    def _off(self, val):
        """Turns the radio off"""
        print('Turning radio off')
        self._write_int(_REG_RFM69_RADIO_STATE, 0)
    
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
        self._write_int(_REG_LED, int(x))

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
    
    @property
    def transceiver_ready(self):
        return bool(self._read_int(_REG_TRANSCEIVER_READY))