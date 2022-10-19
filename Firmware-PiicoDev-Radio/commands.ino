/*
  User accessible functions
*/

void idReturn(char *data) {
  loadArray(valueMap.id);
}

void firmwareMajorReturn(char *data) {
  loadArray(valueMap.firmwareMajor);
}

void firmwareMinorReturn(char *data) {
  loadArray(valueMap.firmwareMinor);
}

void setAddress(char *data) {
  debugln("SetAddress is running");
  uint8_t tempAddress = data[0];

  if (tempAddress < 0x08 || tempAddress > 0x77)
    return; // Command failed. This address is out of bounds.
  valueMap.i2cAddress = tempAddress;

  EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  updateFlag = true; // will trigger a I2C re-initalise and save custom address to EEPROM
}

void getPowerLed(char *data) {
  valueMap.ledRead = digitalRead(powerLedPin);
  loadArray(valueMap.ledRead);
}

void setPowerLed(char *data) {
  powerLed((data[0] == 1));
}

void powerLed(bool state) {
  digitalWrite(powerLedPin, state);
}

void getEncryption(char *data) {

}

void setEncryption(char *data) {

}

void getEncryptionKey(char *data) {

}

void setEncryptionKey(char *data) {

}

void getHighPower(char *data) {

}

void setHighPower(char *data) {

}

void getRfm69RadioState(char *data) {

}

void setRfm69RadioState(char *data) {

}

void getRfm69NodeID(char *data) {
  loadArray(valueMap.rfm69NodeIDRead);
}

void setRfm69NodeID(char *data) {
  valueMap.rfm69NetworkIDRead = data[0];
}

void getRfm69NetworkID(char *data) {
  loadArray(valueMap.rfm69NetworkIDRead);
}

void setRfm69NetworkID(char *data) {
  debugln("------------------------------------------- setchannel called");
  valueMap.rfm69NetworkIDWrite = data[0];
}

void getRfm69ToNodeID(char *data) {
 loadArray(valueMap.rfm69NodeIDRead);
}

void setRfm69ToNodeID(char *data) {
    debugln("------------------------------------------- setDestinationRadioAddress called");
  valueMap.rfm69NodeIDWrite = data[0];
}

void setRfm69Reg(char *data) {

}

void getRfm69Value(char *data) {

}

void setRfm69Value(char *data) {

}

void receivePayloadLength(char *data) {

}

void sendPayloadLength(char *data) {
    debugln("------------------------------------------- setting message length called");
  valueMap.payloadLengthWrite = data[0];
}

void receivePayload(char *data) {

}

void sendPayload(char *data) {
    debug("setMessage data:");
  debugln(data);
//  for (byte i = 0; i < sizeof(data); i++) {
//      ?
//  }
  valueMap.payloadWrite = *data;
  debug("valueMap.payloadWrite:");
  Serial.println(*valueMap.payloadWrite);
}

void getRadioState(char *data) {
  return radioState;
}

void setRadioState(char *data) {
  if (data[0] == 1) {
    radio.initialize(FREQUENCY, valueMap.rfm69NodeIDWrite, valueMap.rfm69NetworkIDWrite);
    radio.setHighPower();
    radio.encrypt(ENCRYPTKEY);
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

void getMessage(char *data) {
  debugln("getMessage Requested");
  if (radio.receiveDone()) {
    debug('[');
    debug(radio.SENDERID);
    debug("] ");
    debug(" [RX_RSSI:");
    debug(radio.readRSSI());
    debug("]");
    //if (spy) Serial.print("to [");Serial.print(radio.TARGETID, DEC);Serial.print("] ");

    if (radio.DATALEN != sizeof(Payload)) {
      debug("Invalid payload received, not matching Payload struct!");
    } else {
      theDataRead = *(Payload *)radio.DATA;  //assume radio.DATA actually contains our struct and not something else
      debug("nodeId=");
      debugln(theDataRead.nodeId);
      debug("message: ");
      debugln(theDataRead.message);
    }
  }
}



// Functions to load data into the response buffer
void loadArray(uint8_t myNumber) {
  for (uint8_t x = 0; x < sizeof(myNumber); x++)
    responseBuffer[x] = (myNumber >> (((sizeof(myNumber) - 1) - x) * 8)) & 0xFF;
  responseSize = sizeof(myNumber);
}

void loadArray(uint16_t myNumber) {
  for (uint8_t x = 0; x < sizeof(myNumber); x++)
    responseBuffer[x] = (myNumber >> (((sizeof(myNumber) - 1) - x) * 8)) & 0xFF;
  responseSize = sizeof(myNumber);
}
