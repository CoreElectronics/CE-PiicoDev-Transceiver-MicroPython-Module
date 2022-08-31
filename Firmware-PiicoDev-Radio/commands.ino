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
    radio.initialize(FREQUENCY, NODEID, NETWORKID);
    //radio.setHighPower();
    radio.encrypt(ENCRYPTKEY);
    radioState = true;
    debugln("Radio turned on");
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

void setMessage(char *data) {
  debugln(data);
  strncpy(theDataWrite.message, data, sizeof(data));
  radio.send(GATEWAYID, (const void *)(&theDataWrite), sizeof(theDataWrite));
  // if (radio.sendWithRetry(GATEWAYID, "hello", 5)) { it's crashing on this line
  //   debugln(" ok!");
  // } else {
  //   debugln(" nothing...");
  // }
  //radio.send(GATEWAYID, "hello", 5);
  debugln("Radio didn't crash");
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