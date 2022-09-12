/*
  User accessible functions
*/

// Macro for number of elements in an array
#define COUNT_OF(x) ((sizeof(x) / sizeof(0 [x])) / ((size_t)(!(sizeof(x) % sizeof(0 [x])))))

// void readPotentiometer(char *data) {
//   #if DEBUG
//     Serial.println(analogRead(potentiometerPin));
//   #endif
//   valueMap.pot = analogRead(potentiometerPin);
//   loadArray((uint16_t)valueMap.pot);
// }

void idReturn(char *data) {
  loadArray((uint16_t)valueMap.id);
}

void firmwareMajorReturn(char *data) {
  loadArray((uint8_t)valueMap.firmwareMajor);
}

void firmwareMinorReturn(char *data) {
  loadArray((uint8_t)valueMap.firmwareMinor);
}

// Control the power LED
void getPowerLed(char *data) {
  valueMap.ledRead = digitalRead(powerLedPin);
  loadArray((uint8_t)valueMap.ledRead);
}

// Control the power LED
void setPowerLed(char *data) {
  powerLed((data[0] == 1));
}

void powerLed(bool state) {
  if (state) {
    digitalWrite(powerLedPin, true);
  } else {
    digitalWrite(powerLedPin, false);
  }
}

void getRadioState(char *data) {
  return radioState;
}

void setRadioState(char *data) {
  if (data[0] == 1) {
    radio.initialize(FREQUENCY, valueMap.radioAddressWrite, valueMap.channelWrite);
    radio.setHighPower();
    radio.encrypt(ENCRYPTKEY);
    radioState = true;
    debug("Radio turned on with address ");
    debug(valueMap.radioAddressWrite);
    debug(" and channel ");
    debugln(valueMap.channelWrite);
  } else {
    radio.sleep();
    radioState = false;
    debugln("Radio turned off");
  }
}

void getRadioAddress(char *data) {
  loadArray((uint8_t)valueMap.radioAddressWrite);
}

void setRadioAddress(char *data) {
  valueMap.radioAddressWrite = data[0];
}
void getChannel(char *data) {
  loadArray((uint8_t)valueMap.channelWrite);
}
void setChannel(char *data) {
  debugln("------------------------------------------- setchannel called");
  valueMap.channelWrite = data[0];
}
void getDestinationRadioAddress(char *data) {
  loadArray((uint8_t)valueMap.destinationRadioAddressWrite);
}
void setDestinationRadioAddress(char *data) {
  debugln("------------------------------------------- setDestinationRadioAddress called");
  valueMap.destinationRadioAddressWrite = data[0];
}

void setMessageLength(char *data) {
  debugln("------------------------------------------- setting message length called");
  valueMap.messageLength = data[0];
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

void setMessage(char *data) {
  debug("setMessage data:");
  debugln(data);
//  for (byte i = 0; i < sizeof(data); i++) {
//      ?
//  }
  valueMap.messageWrite = *data;
  debug("valueMap.messageWrite:");
  Serial.println(*valueMap.messageWrite);
}

void setAddress(char *data) {
  debugln("SetAddress is running");
  uint8_t tempAddress = data[0];

  if (tempAddress < 0x08 || tempAddress > 0x77)
    return;  // Command failed. This address is out of bounds.
  valueMap.i2cAddress = tempAddress;

  EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  updateFlag = true;  // will trigger a I2C re-initalise and save custom address to EEPROM
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
