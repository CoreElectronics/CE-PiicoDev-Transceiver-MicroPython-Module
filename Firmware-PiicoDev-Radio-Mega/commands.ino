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
  debugln("SetAddress is running");
  uint8_t tempAddress = data[0];

  if (tempAddress < 0x08 || tempAddress > 0x77)
    return;  // Command failed. This address is out of bounds.
  valueMap.i2cAddress = tempAddress;

  EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  updateFlag = true;  // will trigger a I2C re-initalise and save custom address to EEPROM
}

void getPowerLed(int numberOfBytesReceived, char *data) {
  valueMap.ledRead = digitalRead(powerLedPin);
  loadArray(valueMap.ledRead);
}

void setPowerLed(int numberOfBytesReceived, char *data) {
  powerLed((data[0] == 1));
}

void powerLed(bool state) {
  digitalWrite(powerLedPin, state);
}

void getHighPower(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.highPowerRead);
}

void setHighPower(int numberOfBytesReceived, char *data) {
  valueMap.highPowerWrite = data[0];
  valueMap.highPowerRead =  data[0];
}

void getRfm69RadioState(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69RadioStateRead);
}

void setRfm69RadioState(int numberOfBytesReceived, char *data) {
  valueMap.rfm69RadioStateWrite = data[0];
  valueMap.rfm69RadioStateRead  = data[0];
  debugln("Running setRadioState");
  if (data[0] == 1) {
    radio.initialize(FREQUENCY, valueMap.rfm69NodeIDWrite, valueMap.rfm69NetworkIDWrite);
    radio.setHighPower();
    //radio.encrypt(ENCRYPTKEY);
    radioState = true;
    debug("Radio turned on with address ");
    debug(valueMap.rfm69NodeIDWrite);
    debug(" and channel ");
    debugln(valueMap.rfm69NetworkIDWrite);
  } else {
    radio.sleep();
    radioState = false;
    debugln("Radio turned off");
  }
}

void getRfm69NodeID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NodeIDRead);
}

void setRfm69NodeID(int numberOfBytesReceived, char *data) {
  valueMap.rfm69NodeIDWrite = data[0];
  valueMap.rfm69NodeIDRead = data[0];
}

void getRfm69NetworkID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NetworkIDRead);
}

void setRfm69NetworkID(int numberOfBytesReceived, char *data) {
  debugln("------------------------------------------- setchannel called");
  valueMap.rfm69NetworkIDWrite = data[0];
  valueMap.rfm69NetworkIDRead = data[0];
}

void getRfm69ToNodeID(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69ToNodeIDRead);
}

void setRfm69ToNodeID(int numberOfBytesReceived, char *data) {
  debugln("------------------------------------------- setDestinationRadioAddress called");
  valueMap.rfm69NodeIDWrite = data[0];
  valueMap.rfm69NodeIDRead = data[0];
}

void setRfm69Reg(int numberOfBytesReceived, char *data) {
  valueMap.rfm69Reg = data[0];      
}

void getRfm69Value(int numberOfBytesReceived, char *data) {
  valueMap.rfm69ValueRead = radio.readReg(valueMap.rfm69Reg);
  loadArray(valueMap.rfm69ValueRead);        
}

void setRfm69Value(int numberOfBytesReceived, char *data) {
  valueMap.rfm69ValueWrite = data[0];
  valueMap.rfm69ValueRead = data[0];
  debug("valueMap.rfm69ValueWrite:");
  debugln(valueMap.rfm69ValueWrite);
  radio.writeReg(valueMap.rfm69Reg, data[0]);   
}

void receivePayloadLength(int numberOfBytesReceived, char *data) {
  debugln("Running Receive Payload Length");
  loadArray(valueMap.payloadLengthRead);
}

void sendPayloadLength(int numberOfBytesReceived, char *data) {
  debugln("Running Send Payload Length");
  valueMap.payloadLengthWrite = data[0];
}

void receivePayload(int numberOfBytesReceived, char *data) {
  debug("Incoming Buffer Size:");
  debugln(payloadBufferIncoming.size());
  debugln(payloadBufferIncoming[1]);
  for (uint8_t x = 0; x < I2C_BUFFER_SIZE ; x++){
    if (!payloadBufferIncoming.isEmpty()) {
      responseBuffer[x] = payloadBufferIncoming.shift();
    }
    debug(responseBuffer[x]);
    debug(",");
  }
  debugln("");
  responseSize = I2C_BUFFER_SIZE;
  debug("Response Size:");
  debugln(responseSize);
}

void sendPayload(int numberOfBytesReceived, char *data) {
  debug("Incoming Data:");
  for (uint8_t x = 0; x < numberOfBytesReceived-1; x++){// without the -1 there will be a null at multiples of the 32nd bit
    debug(data[x]);
    debug(",");
    payloadBufferOutgoing.push(data[x]);
  }
  debugln("");
}

void receivePayloadNew(int numberOfBytesReceived, char *data) {
  loadArray(valueMap.payloadNew);
  valueMap.payloadNew = 0;
} 

void sendPayloadGo(int numberOfBytesReceived, char *data) {
  valueMap.payloadGo = data[0];
  debug("payloadBufferOutgoing.size()");
  debugln(payloadBufferOutgoing.size());
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