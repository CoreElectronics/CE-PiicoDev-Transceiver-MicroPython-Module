_C='BBfB13s'
_B='big'
_A=None
from PiicoDev_Unified import *
import radio_config
from struct import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_BASE_ADDRESS=161
_DEVICE_ID=495
_REG_WHOAMI=1
_REG_FIRM_MAJ=2
_REG_FIRM_MIN=3
_REG_I2C_ADDRESS=4
_REG_LED=5
_REG_ENCRYPTION=17
_REG_ENCRYPTION_KEY=18
_REG_HIGH_POWER=19
_REG_RFM69_RADIO_STATE=20
_REG_RFM69_NODE_ID=21
_REG_RFM69_NETWORK_ID=22
_REG_RFM69_TO_NODE_ID=23
_REG_RFM69_REG=24
_REG_RFM69_VALUE=25
_REG_PAYLOAD_LENGTH=33
_REG_PAYLOAD=34
_REG_PAYLOAD_NEW=35
_REG_PAYLOAD_GO=36
DEBUG=True
def _set_bit(x,n):return x|1<<n
def debug(text):
	if DEBUG:print(text)
class PiicoDev_Radio:
	def __init__(self,bus=_A,freq=_A,sda=_A,scl=_A,address=_BASE_ADDRESS,id=_A,radio_address=radio_config.radio_address,channel=radio_config.channel,suppress_warnings=False):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl,suppress_warnings=suppress_warnings);self._address=address
		if type(id)is list and not all((v==0 for v in id)):assert max(id)<=1 and min(id)>=0 and len(id)==4,'id must be a list of 1/0, length=4';self._address=8+id[0]+2*id[1]+4*id[2]+8*id[3]
		else:self._address=address
		self.radio_address=radio_address;self.channel=channel;self.destination_radio_address=radio_config.destination_radio_address
		try:
			if self.whoami!=_DEVICE_ID:print('* Incorrect device found at address {}'.format(address))
		except:print("* Couldn't find a device - check switches and wiring")
	def _read(self,register,length=1):
		try:return self.i2c.readfrom_mem(self.address,register,length)
		except:print(i2c_err_str.format(self.address));return _A
	def _write(self,register,data):
		try:self.i2c.writeto_mem(self.address,register,data)
		except:print(i2c_err_str.format(self.address))
	def _read_int(self,register,length=1):
		data=self._read(register,length)
		if data is _A:return _A
		else:return int.from_bytes(data,_B)
	def _write_int(self,register,integer,length=1):self._write(register,int.to_bytes(integer,length,_B))
	def send_payload(self,payload):self._write_int(_set_bit(_REG_PAYLOAD_LENGTH,7),len(payload));sleep_ms(10);self._write(_set_bit(_REG_PAYLOAD,7),payload);sleep_ms(10);self._write_int(_set_bit(_REG_PAYLOAD_GO,7),1)
	def receive_payload(self):
		payload=0
		if self._payload_new==1:payload_length=self._read_int(_REG_PAYLOAD_LENGTH);payload=self._read(_REG_PAYLOAD,length=payload_length)
		return payload
	def on(self):self._on=1
	def off(self):self._off=1
	@property
	def encryption(self):return self._read_int(_REG_ENCRYPTION)
	@encryption.setter
	def encryption(self,value):self._write_int(_set_bit(_REG_ENCRYPTION,7),value)
	@property
	def encryption_key(self):return self._read(_REG_ENCRYPTION_KEY)
	@encryption_key.setter
	def encryption_key(self,value):self._write_int(_set_bit(_REG_ENCRYPTION_KEY,7),value)
	@property
	def high_power(self):return self._read_int(_REG_HIGH_POWER)
	@high_power.setter
	def high_power(self,value):self._write_int(_set_bit(_REG_HIGH_POWER,7),value)
	@property
	def rfm69_network_id(self):return self._read_int(_REG_RFM69_NETWORK_ID)
	@rfm69_network_id.setter
	def rfm69_network_id(self,value):print('channel setter called');self._write_int(_set_bit(_REG_RFM69_NETWORK_ID,7),value)
	@property
	def rfm69_node_id(self):return self._read_int(_REG_RFM69_NODE_ID)
	@rfm69_node_id.setter
	def rfm69_node_id(self,value):self._write_int(_set_bit(_REG_RFM69_NODE_ID,7),value)
	@property
	def rfm69_to_node_id(self):return self._read_int(_REG_RFM69_TO_NODE_ID)
	@rfm69_to_node_id.setter
	def rfm69_to_node_id(self,value):debug('Setting destination radio address to '+str(value)+'.');self._write_int(_set_bit(_REG_RFM69_TO_NODE_ID,7),value)
	@property
	def payload_length(self):return 0
	@payload_length.setter
	def payload_length(self,value):debug('Setting message length'+str(value)+'.');self._write_int(_set_bit(_REG_PAYLOAD_LENGTH,7),value)
	@property
	def _payload_new(self):return self._read_int(_REG_PAYLOAD_NEW)
	def receive(self):
		data=0;payload=self.receive_payload()
		if payload!=0:data=unpack(_C,bytes(payload))
		return data
	def send(self,message_string,value=0.0,destination_radio_address=0):data=pack(_C,self.radio_address,destination_radio_address,value,len(message_string),bytes(message_string,'utf8'));self.send_payload(data)
	def send_byte(self,value):data=pack('B',value);self.send_payload(data)
	def receive_byte(self):
		data=0;payload=self.receive_payload()
		if payload!=0:data=int.from_bytes(payload,_B)
		return data
	@property
	def _on(self):'Checks the radio state';self._read_int(_REG_RFM69_RADIO_STATE,1)
	@_on.setter
	def _on(self,val):'Turns the radio on';print('Turning radio on!');self._write_int(_set_bit(_REG_RFM69_RADIO_STATE,7),1)
	@property
	def _off(self):'Checks the radio state';print('Turning radio off');self._read_int(_REG_RFM69_RADIO_STATE,0)
	@_off.setter
	def _off(self,val):'Turns the radio off';self._write_int(_set_bit(_REG_RFM69_RADIO_STATE,7),0)
	@property
	def address(self):'Returns the currently configured 7-bit I2C address';return self._address
	@property
	def led(self):'Returns the state onboard "Power" LED. `True` / `False`';return bool(self._read_int(_REG_LED))
	@led.setter
	def led(self,x):'control the state onboard "Power" LED. accepts `True` / `False`';self._write_int(_set_bit(_REG_LED,7),int(x))
	@property
	def whoami(self):'returns the device identifier';return self._read_int(_REG_WHOAMI,2)
	@property
	def firmware(self):'Returns the firmware version';v=[0,0];v[1]=self._read_int(_REG_FIRM_MAJ);v[0]=self._read_int(_REG_FIRM_MIN);return v[1],v[0]
	def setI2Caddr(self,newAddr):x=int(newAddr);assert 8<=x<=119,'address must be >=0x08 and <=0x77';self._write_int(_REG_I2C_ADDRESS,x);self._address=x;sleep_ms(5);return 0