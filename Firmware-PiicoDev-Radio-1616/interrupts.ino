// Executes when data is received on I2C
// this function is registered as an event, see setup() and/or startI2C()
void receiveEvent(int numberOfBytesReceived)
{
  lastSyncTime = millis();
  incomingDataSpot = 0;
  debugln("Interrupt Function Running----------------------------------");
  memset(incomingData, 0, sizeof(incomingData));
  while (Wire.available())
  {
    currentRegisterNumber = Wire.read();
    while (Wire.available())
    {
      incomingData[incomingDataSpot++] = Wire.read();
      //debug("IncomingDataI2CInterrupt:");
      //debugln(char(incomingData[incomingDataSpot-1]));
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

void requestEvent() {
  lastSyncTime = millis();
  Wire.write(responseBuffer, responseSize);
}
