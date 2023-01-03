// Executes when data is received on I2C
// this function is registered as an event, see setup() and/or startI2C()
void receiveEvent(int numberOfBytesReceived)
{
  lastSyncTime = millis();
  incomingDataSpot = 0;
  if (Wire.available() > 0) {  // Don't run unless there is data - on ATtiny1616 receiveEvent is triggered twice instead on once for each I2C transaction.
    memset(incomingData, 0, sizeof(incomingData));
    while (Wire.available() > 0)
    {
      currentRegisterNumber = Wire.read();
      while (Wire.available() > 0)
      {
        incomingData[incomingDataSpot++] = Wire.read();
        //incomingData is 32 bytes. We shouldn't spill over because receiveEvent can't receive more than 32 bytes
      }
    }
    for (uint16_t regNum = 0; regNum < (sizeof(memoryMapRegs) / sizeof(uint8_t)); regNum++)
    {
      if (functions[regNum].registerNumber == currentRegisterNumber)
      {
        functions[regNum].handleFunction(numberOfBytesReceived, (char *)incomingData);
        break; // guarantee only one match (first matching register number)
      }
    }
  }
}

void requestEvent() {
  lastSyncTime = millis();
  Wire.write(responseBuffer, responseSize);
}
