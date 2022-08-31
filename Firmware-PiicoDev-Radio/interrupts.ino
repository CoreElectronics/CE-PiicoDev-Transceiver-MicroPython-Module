// Executes when data is received on I2C
// this function is registered as an event, see setup() and/or startI2C()
void receiveEvent(uint16_t numberOfBytesReceived)
{
  lastSyncTime = millis();
  incomingDataSpot = 0;

  memset(incomingData, 0, sizeof(incomingData));
  while (Wire.available())
  {
    currentRegisterNumber = Wire.read();
    while (Wire.available())
    {
      incomingData[incomingDataSpot++] = Wire.read();
      #if DEBUG
      Serial.print(char(incomingData[incomingDataSpot-1]), HEX);
      //incomingData is 32 bytes. We shouldn't spill over because receiveEvent can't receive more than 32 bytes
      #endif
    }
  }
  for (uint16_t regNum = 0; regNum < (sizeof(memoryMap) / sizeof(uint8_t)); regNum++)
  {
    if (functions[regNum].registerNumber == currentRegisterNumber)
    {
      functions[regNum].handleFunction(incomingData);
    }
  }
}

void requestEvent() {
  lastSyncTime = millis();
  Wire.write(responseBuffer, responseSize);
}
