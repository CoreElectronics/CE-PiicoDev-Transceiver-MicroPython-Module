/*
  User accessible functions
*/

void idReturn(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.id);
}

void firmwareMajorReturn(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.firmwareMajor);
}

void firmwareMinorReturn(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.firmwareMinor);
}

void setAddress(int numberOfBytesReceived, char *data) {
  uint8_t tempAddress = data[0];

  if (tempAddress < 0x08 || tempAddress > 0x77)
    return;  // Command failed. This address is out of bounds.
  valueMap.i2cAddress = tempAddress;

  EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  updateFlag = true;  // will trigger a I2C re-initalise and save custom address to EEPROM
}

void getPowerLed(int numberOfBytesReceived, char *data) {
  valueMap.led = digitalRead(powerLedPin);
  loadArray(valueMap.led);
}

void setPowerLed(int numberOfBytesReceived, char *data) {
  powerLed((data[0] == 1));
}

void powerLed(bool state) {
  digitalWrite(powerLedPin, state);
}

uint8_t twosComplementEncode(int8_t value) {
  return -(~value + 1);
}

int8_t twosComplementDecode(uint8_t value) {
  return -(~(value - 1));
}

void getTxPower(int numberOfBytesReceived, char *data) {
  loadArray(twosComplementEncode(valueMap.txPower));
}

void setTxPower(int numberOfBytesReceived, char *data) {
  valueMap.txPower = twosComplementDecode(data[0]);
  radioSetPower = true;
}

void getRfm69RadioState(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69RadioState);
}

void setRfm69RadioState(int numberOfBytesReceived, char *data) {
  valueMap.rfm69RadioState = data[0];
  if (data[0] == 1) {
    radioInitialise = true;
  } else {
    radio.sleep();
  }
}

void getRfm69NodeID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NodeID);
}

void setRfm69NodeID(int numberOfBytesReceived, char *data) {
  valueMap.rfm69NodeID = data[0] << 8 | data[1];
  radioInitialise = true;
}

void getRfm69NetworkID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NetworkID);
}

void setRfm69NetworkID(int numberOfBytesReceived, char *data) {
  valueMap.rfm69NetworkID = data[0];
  radioInitialise = true;
}

void getRfm69ToNodeID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69ToNodeID);
}

void setRfm69ToNodeID(int numberOfBytesReceived, char *data) {
  valueMap.rfm69ToNodeID = data[0] << 8 | data[1];
}

void setRfm69Reg(int numberOfBytesReceived, char *data) {
  valueMap.rfm69Reg = data[0];      
}

void getRfm69Value(int numberOfBytesReceived, char *data) {
  valueMap.rfm69Value = radio.readReg(valueMap.rfm69Reg);
  loadArray(valueMap.rfm69Value);        
}

void setRfm69Value(int numberOfBytesReceived, char *data) {
  valueMap.rfm69Value = data[0];
  radio.writeReg(valueMap.rfm69Reg, data[0]);   
}

void setRfm69Reset(int numberOfBytesReceived, char *data) {
  radioReset = true;
}

void receivePayloadLength(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.payloadLength);
}

void sendPayloadLength(int numberOfBytesReceived, char *data) {
  valueMap.payloadLength = data[0];
}

void receivePayload(int numberOfBytesReceived, char *data) {
  for (uint8_t x = 0; x < I2C_BUFFER_SIZE ; x++){
    if (!payloadBufferIncoming.isEmpty()) {
      responseBuffer[x] = payloadBufferIncoming.shift();
    }
  }
  responseSize = I2C_BUFFER_SIZE;
}

void sendPayload(int numberOfBytesReceived, char *data) {
  uint8_t lengthToProcess;
  if (numberOfBytesReceived == I2C_BUFFER_SIZE){
    lengthToProcess = I2C_BUFFER_SIZE - 1; // without the -1 there will be a null at multiples of the 32nd bit
  } else {
    lengthToProcess = numberOfBytesReceived;
  }
  for (uint8_t x = 0; x < lengthToProcess; x++){
    payloadBufferOutgoing.push(data[x]);
  }
}

void receivePayloadNew(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.payloadNew);
  valueMap.payloadNew = 0;
} 

void sendPayloadGo(int numberOfBytesReceived, char *data) {
  valueMap.payloadGo = data[0];
}

void getTransceiverReady(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.transceiverReady);
}

// Functions to load data into the response buffer
void loadArray(uint8_t myNumber) {
  responseBuffer[0] = myNumber;
  responseSize = sizeof(myNumber);
}

void loadArray(uint16_t myNumber) {
  responseBuffer[0] = (myNumber >> 8) & 0xFF;
  responseBuffer[1] = myNumber & 0xFF;
  responseSize = sizeof(myNumber);
}
