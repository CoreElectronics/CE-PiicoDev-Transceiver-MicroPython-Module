/*
  User accessible functions
*/

void idReturn(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.id);
}

void firmwareMajorReturn(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.firmwareMajor);
}

void firmwareMinorReturn(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.firmwareMinor);
}

void setAddress(uint8_t numberOfBytesReceived, char *data) {
  debugln("SetAddress is running");
  uint8_t tempAddress = data[0];

  if (tempAddress < 0x08 || tempAddress > 0x77)
    return;  // Command failed. This address is out of bounds.
  valueMap.i2cAddress = tempAddress;

  EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  updateFlag = true;  // will trigger a I2C re-initalise and save custom address to EEPROM
}

void getPowerLed(uint8_t numberOfBytesReceived, char *data) {
  valueMap.ledRead = digitalRead(powerLedPin);
  loadArray(valueMap.ledRead);
}

void setPowerLed(uint8_t numberOfBytesReceived, char *data) {
  powerLed((data[0] == 1));
}

void powerLed(bool state) {
  digitalWrite(powerLedPin, state);
}

void getEncryption(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.encryptionRead);
}

void setEncryption(uint8_t numberOfBytesReceived, char *data) {
  // valueMap.encryptionWrite[0] = data[0];
  // valueMap.encryptionWrite[1] = data[1];
  // valueMap.encryptionRead[0] = data[0];
  // valueMap.encryptionRead[1] = data[1];
}

void getEncryptionKey(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.encryptionKeyRead);
  debug("encryotion key: ");
  debugln(valueMap.encryptionKeyRead);
}

void setEncryptionKey(uint8_t numberOfBytesReceived, char *data) {
  valueMap.encryptionKeyWrite = data[0];
  valueMap.encryptionKeyRead = data[0];
}

void getHighPower(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.highPowerRead);
}

void setHighPower(uint8_t numberOfBytesReceived, char *data) {
  valueMap.highPowerWrite = data[0];
  valueMap.highPowerRead =  data[0];
}

void getRfm69RadioState(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69RadioStateRead);
}

void setRfm69RadioState(uint8_t numberOfBytesReceived, char *data) {
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

void getRfm69NodeID(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NodeIDRead);
}

void setRfm69NodeID(uint8_t numberOfBytesReceived, char *data) {
  valueMap.rfm69NodeIDWrite = data[0];
  valueMap.rfm69NodeIDRead = data[0];
}

void getRfm69NetworkID(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69NetworkIDRead);
}

void setRfm69NetworkID(uint8_t numberOfBytesReceived, char *data) {
  debugln("------------------------------------------- setchannel called");
  valueMap.rfm69NetworkIDWrite = data[0];
  valueMap.rfm69NetworkIDRead = data[0];
}

void getRfm69ToNodeID(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.rfm69ToNodeIDRead);
}

void setRfm69ToNodeID(uint8_t numberOfBytesReceived, char *data) {
  debugln("------------------------------------------- setDestinationRadioAddress called");
  valueMap.rfm69NodeIDWrite = data[0];
  valueMap.rfm69NodeIDRead = data[0];
}

void setRfm69Reg(uint8_t numberOfBytesReceived, char *data) {
  valueMap.rfm69Reg = data[0];      
}

void getRfm69Value(uint8_t numberOfBytesReceived, char *data) {
  valueMap.rfm69ValueRead = radio.readReg(valueMap.rfm69Reg);
  loadArray(valueMap.rfm69ValueRead);        
}

void setRfm69Value(uint8_t numberOfBytesReceived, char *data) {
  valueMap.rfm69ValueWrite = data[0];
  valueMap.rfm69ValueRead = data[0];
  debug("valueMap.rfm69ValueWrite:");
  debugln(valueMap.rfm69ValueWrite);
  radio.writeReg(valueMap.rfm69Reg, data[0]);   
}

void receivePayloadLength(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.payloadLengthRead);
}

void sendPayloadLength(uint8_t numberOfBytesReceived, char *data) {
  valueMap.payloadLengthWrite = data[0];
}

void receivePayload(uint8_t numberOfBytesReceived, char *data) {
  //debugln(valueMap.payloadLengthRead);
  //debugln(valueMap.payloadRead);
  debug("Incoming Buffer Size:");
  debugln(payloadBufferIncoming.size());
  debugln("------------");
  debug("Head:");
  debug(payloadBufferIncoming.first());
  debugln(payloadBufferIncoming[1]);
  for (uint8_t x = 0; x < I2C_BUFFER_SIZE ; x++){
    if (!payloadBufferIncoming.isEmpty()) {
      responseBuffer[x] = payloadBufferIncoming.shift();
    } else {
      responseBuffer[x] = 0; // pad with zeros
    }
    debug(responseBuffer[x]);
    debug(",");
  }
  debugln("");
  //memcpy(responseBuffer, valueMap.payloadRead, valueMap.payloadLengthRead);
  responseSize = I2C_BUFFER_SIZE;  //valueMap.payloadLengthRead;
  debug("Response Size:");
  debugln(responseSize);
}

void sendPayload(uint8_t numberOfBytesReceived, char *data) {
  debug("Incoming Data:");
  for (uint8_t x = 0; x < numberOfBytesReceived-1; x++){// without the -1 there will be a null at multiples of the 32nd bit
    debug(data[x]);
    debug(",");
    payloadBufferOutgoing.push(data[x]);
  }
  debugln("");
}

void receivePayloadNew(uint8_t numberOfBytesReceived, char *data) {
  loadArray(valueMap.payloadNew);
  valueMap.payloadNew = 0;
} 

void sendPayloadGo(uint8_t numberOfBytesReceived, char *data) {
  valueMap.payloadGo = data[0];
  debug("payloadBufferOutgoing.size()");
  debugln(payloadBufferOutgoing.size());
} 

// void getMessage(char *data) {
//   debugln("getMessage Requested");
//   if (radio.receiveDone()) {
//     debug('[');
//     debug(radio.SENDERID);
//     debug("] ");
//     debug(" [RX_RSSI:");
//     debug(radio.readRSSI());
//     debug("]");
//     //if (spy) Serial.print("to [");Serial.print(radio.TARGETID, DEC);Serial.print("] ");

//     if (radio.DATALEN != sizeof(Payload)) {
//       debug("Invalid payload received, not matching Payload struct!");
//     } else {
//       theDataRead = *(Payload *)radio.DATA;  //assume radio.DATA actually contains our struct and not something else
//       debug("nodeId=");
//       debugln(theDataRead.nodeId);
//       debug("message: ");
//       debugln(theDataRead.message);
//     }
//   }
// }

// Functions to load data into the response buffer
void loadArray(uint8_t myNumber) {
  // for (uint8_t x = 0; x < sizeof(myNumber); x++)
  //   responseBuffer[x] = (myNumber >> (((sizeof(myNumber) - 1) - x) * 8)) & 0xFF;
  // responseSize = sizeof(myNumber);
  responseBuffer[0] = myNumber;
  responseSize = sizeof(myNumber);
}

void loadArray(uint16_t myNumber) {
  // for (uint8_t x = 0; x < sizeof(myNumber); x++)
  //   responseBuffer[x] = (myNumber >> (((sizeof(myNumber) - 1) - x) * 8)) & 0xFF;
  // responseSize = sizeof(myNumber);

  responseBuffer[0] = (myNumber >> 8) & 0xFF;
  responseBuffer[1] = myNumber & 0xFF;
  responseSize = sizeof(myNumber);
}

// void loadArray(char* myNumber) {
//   for (uint8_t x = 0; x < sizeof(myNumber); x++)
//     responseBuffer[x] = ((uint16_t)myNumber >> (((sizeof(myNumber) - 1) - x) * 8)) & 0xFF;
//   responseSize = sizeof(myNumber);
// }