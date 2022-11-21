// Reads the current system settings from EEPROM
// Resets to default if anything is unusual

void readSystemSettings(void)
{
  //Read what I2C address we should use
  unsigned char i2cAddress = valueMap.i2cAddress;
  EEPROM.get(LOCATION_I2C_ADDRESS, i2cAddress);
  valueMap.i2cAddress = i2cAddress;

  if (valueMap.i2cAddress == 255)
  {
    valueMap.i2cAddress = DEFAULT_I2C_ADDRESS; //By default, we listen for DEFAULT_I2C_ADDRESS
    EEPROM.put(LOCATION_I2C_ADDRESS, DEFAULT_I2C_ADDRESS);
  }

  //Error check I2C address we read from EEPROM
  if (valueMap.i2cAddress < 0x08 || valueMap.i2cAddress > 0x77)
  {
    //User has set the address out of range
    //Go back to defaults
    valueMap.i2cAddress = DEFAULT_I2C_ADDRESS;
    EEPROM.put(LOCATION_I2C_ADDRESS, DEFAULT_I2C_ADDRESS);
  }
}

//If the current setting is different from that in EEPROM, update EEPROM
void recordSystemSettings(void)
{
  //I2C address is byte
  uint8_t i2cAddr;

  //Error check the current I2C address
  if (valueMap.i2cAddress >= 0x08 && valueMap.i2cAddress <= 0x77) {
    //Address is valid
    //Read the value currently in EEPROM. If it's different from the memory map then record the memory map value to EEPROM.
    EEPROM.get(LOCATION_I2C_ADDRESS, i2cAddr);
    if (i2cAddr != valueMap.i2cAddress)
    {
      EEPROM.put(LOCATION_I2C_ADDRESS, (uint8_t)valueMap.i2cAddress);
    }
  } else {
    EEPROM.get(LOCATION_I2C_ADDRESS, i2cAddr);
    valueMap.i2cAddress = i2cAddr; //Return to original address
  }
}
