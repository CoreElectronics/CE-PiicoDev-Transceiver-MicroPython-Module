_D='utf8'
_C='big'
_B=False
_A=None
from PiicoDev_Unified import *
from struct import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_BASE_ADDRESS=26
_DEVICE_ID=495
_REG_WHOAMI=1
_REG_FIRM_MAJ=2
_REG_FIRM_MIN=3
_REG_I2C_ADDRESS=4
_REG_LED=5
_REG_TX_POWER=19
_REG_RFM69_RADIO_STATE=20
_REG_RFM69_NODE_ID=21
_REG_RFM69_NETWORK_ID=22
_REG_RFM69_TO_NODE_ID=23
_REG_RFM69_REG=24
_REG_RFM69_VALUE=25
_REG_RFM69_RESET=32
_REG_PAYLOAD_LENGTH=33
_REG_PAYLOAD=34
_REG_PAYLOAD_NEW=35
_REG_PAYLOAD_GO=36
_REG_TRANSCEIVER_READY=37
_RFM69_REG_BITRATEMSB=3
_RFM69_REG_BITRATELSB=4
_RFM69_REG_FRFMSB=7
_RFM69_REG_FRFMID=8
_RFM69_REG_FRFLSB=9
_MAXIMUM_PAYLOAD_LENGTH=61
_MAXIMUM_I2C_SIZE=32
def truncate(n,decimals=0):multiplier=10**decimals;return int(n*multiplier)/multiplier
def _set_bit(x,n):return x|1<<n
class PiicoDev_Transceiver:
	def __init__(self,bus=_A,freq=_A,sda=_A,scl=_A,address=_BASE_ADDRESS,id=_A,channel=0,radio_address=1,speed=2,radio_frequency=922,tx_power=20,suppress_warnings=_B,debug=_B):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl,suppress_warnings=suppress_warnings);self._address=address
		if type(id)is list and not all((v==0 for v in id)):assert max(id)<=1 and min(id)>=0 and len(id)==4,'id must be a list of 1/0, length=4';self._address=8+id[0]+2*id[1]+4*id[2]+8*id[3]
		else:self._address=address
		if radio_address<0:radio_address=0
		if radio_address>127:radio_address=127
		if channel<0:channel=0
		if channel>255:channel=255
		self.debug=debug
		if self.debug:print('start updating radio');sleep_ms(3000);print('radio left alone for 3 seconds')
		while self.transceiver_ready==_B:sleep_ms(10);print(self.transceiver_ready)
		self._write_int(_REG_RFM69_NODE_ID,radio_address,2)
		if self.debug:sleep_ms(3000)
		while self.transceiver_ready==_B:sleep_ms(10)
		self._write_int(_REG_RFM69_NETWORK_ID,channel);self.rssi=0;self.type=0;self.message='';self.key='';self.value=_A;self.received_bytes=b'';self.source_radio_address=0;self.radio_frequency=radio_frequency;self.speed=speed;self.tx_power=tx_power
		try:
			if self.whoami!=_DEVICE_ID:print('* Incorrect device found at address {}'.format(address))
		except:print("* Couldn't find a device - check switches and wiring")
	def _read(self,register,length=1):
		try:return self.i2c.readfrom_mem(self.address,register,length)
		except:print(i2c_err_str.format(self.address));return _A
	def _write(self,register,data):
		try:self.i2c.writeto_mem(self.address,_set_bit(register,7),data)
		except:print(i2c_err_str.format(self.address))
	def _read_int(self,register,length=1):
		data=self._read(register,length)
		if data is _A:return _A
		else:return int.from_bytes(data,_C)
	def _write_int(self,register,integer,length=1):self._write(register,int.to_bytes(integer,length,_C))
	def send_payload(self,payload):
		payload_list=[payload[i:i+_MAXIMUM_I2C_SIZE-1]for i in range(0,len(payload),_MAXIMUM_I2C_SIZE-1)];self._write_int(_REG_PAYLOAD_LENGTH,len(payload));sleep_ms(5)
		for i in range(len(payload_list)):self._write(_REG_PAYLOAD,payload_list[i]);sleep_ms(5)
		self._write_int(_REG_PAYLOAD_GO,1)
	def receive_payload(self):
		payload_length=0;payload=bytes(0)
		if self._payload_new==1:
			if self.debug:sleep_ms(100);print('delay')
			payload_length=self._read_int(_REG_PAYLOAD_LENGTH)+3;unprocessed_payload_length=payload_length;sleep_ms(5);number_of_chunks=int(truncate(payload_length/_MAXIMUM_I2C_SIZE))+1
			for i in range(number_of_chunks):
				chunk_length=_MAXIMUM_I2C_SIZE
				if unprocessed_payload_length<32:chunk_length=unprocessed_payload_length
				if chunk_length>0:payload=payload+bytes(self._read(_REG_PAYLOAD,length=chunk_length))
				unprocessed_payload_length-=_MAXIMUM_I2C_SIZE;sleep_ms(5)
			payload=payload[:payload_length]
		return payload_length,payload
	def on(self):self._on=1
	def off(self):self._off=1
	@property
	def tx_power(self):
		while self.transceiver_ready==_B:sleep_ms(10)
		value=unpack('b',bytes(self._read(_REG_TX_POWER)));return value[0]
	@tx_power.setter
	def tx_power(self,value):
		if value<-2:value=-2
		if value>20:value=20
		while self.transceiver_ready==_B:sleep_ms(10)
		self._write(_REG_TX_POWER,pack('b',value))
	@property
	def channel(self):' There is no setter because we only want to set when initialising because changing this will trigger a re-initialise in the arduino';return self._read_int(_REG_RFM69_NETWORK_ID)
	@property
	def radio_address(self):' There is no setter because we only want to set when initialising because changing this will trigger a re-initialise in the arduino';return self._read_int(_REG_RFM69_NODE_ID,2)
	@property
	def destination_radio_address(self):return self._read_int(_REG_RFM69_TO_NODE_ID,2)
	@destination_radio_address.setter
	def destination_radio_address(self,value):
		if value<0:return
		if value>127:return
		self._write_int(_REG_RFM69_TO_NODE_ID,value,2)
	def rfm69_reset(self):self._write_int(_REG_RFM69_RESET,1);sleep_ms(10)
	@property
	def payload_length(self):return 0
	@payload_length.setter
	def payload_length(self,value):self._write_int(_REG_PAYLOAD_LENGTH,value)
	@property
	def _payload_new(self):return self._read_int(_REG_PAYLOAD_NEW)
	def receive(self):
		payload_length,payload=self.receive_payload()
		if payload_length!=0:
			payload_bytes=bytes(payload);self.rssi=-int.from_bytes(payload_bytes[:1],_C);self.source_radio_address=int.from_bytes(payload_bytes[1:3],_C);self.type=int.from_bytes(payload_bytes[3:4],_C)
			try:
				if self.type==1:self.key=str(payload_bytes[9:],_D);self.value=unpack('>i',payload_bytes[4:8])[0]
				if self.type==2:self.key=str(payload_bytes[9:],_D);self.value=unpack('>f',payload_bytes[4:8])[0]
				if self.type==3:self.message=str(payload_bytes[5:],_D)
			except:print('* error parsing payload')
			return True
		return _B
	def send(self,message_string,value=_A,address=0):
		A='s';self.destination_radio_address=address;sleep_ms(8)
		if isinstance(value,int):type=1;message_string=message_string[:_MAXIMUM_PAYLOAD_LENGTH-6];format_characters='>BiB'+str(len(message_string))+A;data=pack(format_characters,type,value,len(message_string),bytes(message_string,_D))
		if isinstance(value,float):type=2;message_string=message_string[:_MAXIMUM_PAYLOAD_LENGTH-6];format_characters='>BfB'+str(len(message_string))+A;data=pack(format_characters,type,value,len(message_string),bytes(message_string,_D))
		if value is _A:type=3;message_string=message_string[:_MAXIMUM_PAYLOAD_LENGTH-2];format_characters='>BB'+str(len(message_string))+A;data=pack(format_characters,type,len(message_string),bytes(message_string,_D))
		self.send_payload(data)
	def send_bytes(self,data,address=0):self.destination_radio_address=address;self.send_payload(data)
	def receive_bytes(self):
		payload_length,payload=self.receive_payload()
		if payload_length!=0:payload_bytes=bytes(payload);self.rssi=-int.from_bytes(payload_bytes[:1],_C);self.source_radio_address=int.from_bytes(payload_bytes[1:3],_C);self.received_bytes=payload_bytes[3:];return True
		return _B
	def get_rfm69_register(self,register):self._write_int(_REG_RFM69_REG,register);return self._read_int(_REG_RFM69_VALUE)
	def set_rfm69_register(self,register,value):self._write_int(_REG_RFM69_REG,register);self._write_int(_REG_RFM69_VALUE,value)
	@property
	def radio_frequency(self):return self._radio_frequency
	@radio_frequency.setter
	def radio_frequency(self,frequency):
		while self.transceiver_ready==_B:sleep_ms(10)
		if frequency==915:sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMSB,228);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMID,192);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFLSB,0);sleep_ms(5);self._radio_frequency=915
		elif frequency==918:sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMSB,229);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMID,128);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFLSB,0);sleep_ms(5);self._radio_frequency=918
		elif frequency==922:sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMSB,230);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMID,128);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFLSB,0);sleep_ms(5);self._radio_frequency=922
		elif frequency==925:sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMSB,231);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMID,64);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFLSB,0);sleep_ms(5);self._radio_frequency=925
		elif frequency==928:sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMSB,232);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFMID,0);sleep_ms(5);self.set_rfm69_register(_RFM69_REG_FRFLSB,0);sleep_ms(5);self._radio_frequency=928
		else:print(' * frequency not supported')
	@property
	def speed(self):return self._speed
	@speed.setter
	def speed(self,speed):
		if speed==1:sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATEMSB,13);sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATELSB,5);sleep_ms(10);self._speed=1
		elif speed==2:sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATEMSB,1);sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATELSB,22);sleep_ms(10);self._speed=2
		elif speed==3:sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATEMSB,0);sleep_ms(10);self.set_rfm69_register(_RFM69_REG_BITRATELSB,107);sleep_ms(10);self._speed=3
		else:print('* speed not valid')
	@property
	def _on(self):'Checks the radio state';self._read_int(_REG_RFM69_RADIO_STATE,1);sleep_ms(5)
	@_on.setter
	def _on(self,val):'Turns the radio on';sleep_ms(5);self._write_int(_REG_RFM69_RADIO_STATE,1);sleep_ms(5)
	@property
	def _off(self):'Checks the radio state';self._read_int(_REG_RFM69_RADIO_STATE,0);sleep_ms(5)
	@_off.setter
	def _off(self,val):'Turns the radio off';sleep_ms(5);self._write_int(_REG_RFM69_RADIO_STATE,0);sleep_ms(5)
	@property
	def address(self):'Returns the currently configured 7-bit I2C address';return self._address
	@property
	def led(self):'Returns the state onboard "Power" LED. `True` / `False`';return bool(self._read_int(_REG_LED))
	@led.setter
	def led(self,x):'control the state onboard "Power" LED. accepts `True` / `False`';self._write_int(_REG_LED,int(x))
	@property
	def whoami(self):'returns the device identifier';return self._read_int(_REG_WHOAMI,2)
	@property
	def firmware(self):'Returns the firmware version';v=[0,0];v[1]=self._read_int(_REG_FIRM_MAJ);v[0]=self._read_int(_REG_FIRM_MIN);return v[1],v[0]
	def setI2Caddr(self,newAddr):x=int(newAddr);assert 8<=x<=119,'address must be >=0x08 and <=0x77';self._write_int(_REG_I2C_ADDRESS,x);self._address=x;sleep_ms(5);return 0
	@property
	def transceiver_ready(self):return bool(self._read_int(_REG_TRANSCEIVER_READY))