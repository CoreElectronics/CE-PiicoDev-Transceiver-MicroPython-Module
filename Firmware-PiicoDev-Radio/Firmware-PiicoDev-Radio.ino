/*
   PiicoDev Radio Firmware
   Written by Peter Johnston @ Core Electronics
   Based off the Core Electronics Buzzer module https://github.com/CoreElectronics/CE-PiicoDev-Buzzer-MicroPython-Module
   Based off work by Felix Rusu 2018, http://www.LowPowerLab.com/contact
   Date: AUGUST 2022
   An I2C based module that utilises an RFM69 radio

   Feel like supporting PiicoDev? Buy a module here:
   Radio: https://core-electronics.com.au/catalog/product/view/sku/CE08757

*/

#include <RFM69.h>         //get it here: https://www.github.com/lowpowerlab/rfm69
//#include <RFM69_ATC.h>     //get it here: https://www.github.com/lowpowerlab/rfm69
//#include <SPIFlash.h>      //get it here: https://www.github.com/lowpowerlab/spiflash
#include <SPI.h>           //included with Arduino IDE install (www.arduino.cc)

#define DEBUG true
#if DEBUG == true
#define debug(x)     Serial.print(x)
#define debugln(x)   Serial.println(x)
#else
#define debug(x)
#define debugln(x)
#endif

#include <Wire.h>
#include <EEPROM.h>
#include <stdint.h>
#include <avr/sleep.h> // For sleep_mode
#include <avr/power.h> // For powering-down peripherals such as ADC and Timers

#define FIRMWARE_MAJOR 0x01
#define FIRMWARE_MINOR 0x00
#define DEVICE_ID 495
#define DEFAULT_I2C_ADDRESS 0xA1    // The default address when all switches are off
#define I2C_ADDRESS_POOL_START 0x08 // The start of the 'smart module address pool' minus 1 - addresses settable by switches
#define SOFTWARE_ADDRESS true
#define HARDWARE_ADDRESS false
#define I2C_BUFFER_SIZE 32 //For ATmega328 based Arduinos, the I2C buffer is limited to 32 bytes
#define FREQUENCY RF69_915MHZ
//#define MYNODEID      1
//#define NETWORKID   0
//#define TONODEID   2
#define ENCRYPTKEY    "-PiicoDevRadio- " //has to be same 16 characters/bytes on all nodes, not more not less!

RFM69 radio;

enum eepromLocations {
  LOCATION_I2C_ADDRESS = 0x00,  // Device's address
  LOCATION_ADDRESS_TYPE = 0x01, // Address type can be either hardware defined (jumpers/switches), or software defined by user.
};

uint8_t oldAddress;

// Hardware Connectins
// Prototyping with Arduino Uno
#if defined(__AVR_ATmega328P__)
const uint8_t powerLedPin = 3;
const uint16_t addressPin1 = 8;
const uint16_t addressPin2 = 7;
const uint16_t addressPin3 = 6;
const uint16_t addressPin4 = 5;
#else
// ATTINY 8x6 or 16x6
const uint8_t powerLedPin = PIN_PA3;
const uint8_t addressPin1 = PIN_PA1;
const uint8_t addressPin2 = PIN_PC3;
const uint8_t addressPin3 = PIN_PC2;
const uint8_t addressPin4 = PIN_PC1;
#endif

// System global variables
volatile bool updateFlag = true; // Goes true when new data received. Cause LEDs to update
volatile uint32_t lastSyncTime = 0;

#define LOCAL_BUFFER_SIZE 20 // bytes
uint8_t incomingData[LOCAL_BUFFER_SIZE]; // Local buffer to record I2C bytes before committing to file, add 1 for 0 character on end
volatile uint16_t incomingDataSpot = 0; // Keeps track of where we are in the incoming buffer

uint8_t responseBuffer[I2C_BUFFER_SIZE]; // Used to pass data back to master
volatile uint8_t responseSize = 1; // Defines how many bytes of relevant data is contained in the responseBuffer

bool radioState = false;

struct memoryMap {
  uint16_t id;
  uint8_t firmwareMajor;
  uint8_t firmwareMinor;
  uint8_t i2cAddress;
  uint8_t ledRead;
  uint8_t ledWrite;
  uint8_t radioStateRead;
  uint8_t radioStateWrite;
  uint8_t radioAddressRead;
  uint8_t radioAddressWrite;
  uint8_t channelRead;
  uint8_t channelWrite;
  uint8_t destinationRadioAddressRead;
  uint8_t destinationRadioAddressWrite;
  uint16_t messageLength;
  uint8_t *messageRead;
  uint8_t *messageWrite;
};

// Register addresses.
const memoryMap registerMap = {
  .id = 0x11,
  .firmwareMajor = 0x02,
  .firmwareMinor = 0x03,
  .i2cAddress = 0x04,
  .ledRead = 0x05,
  .ledWrite = 0x85,
  .radioStateRead = 0x06,
  .radioStateWrite = 0x86,
  .radioAddressRead = 0x07,
  .radioAddressWrite = 0x87,
  .channelRead = 0x08,
  .channelWrite = 0x88,
  .destinationRadioAddressRead = 0x09,
  .destinationRadioAddressWrite = 0x89,
  .messageLength = 0x8A,
  .messageRead = 0x21,
  .messageWrite = 0xA1
};

volatile memoryMap valueMap = {
  .id = DEVICE_ID,
  .firmwareMajor = FIRMWARE_MAJOR,
  .firmwareMinor = FIRMWARE_MINOR,
  .i2cAddress = DEFAULT_I2C_ADDRESS,
  .ledRead = 0x01,
  .ledWrite = 0x01,
  .radioStateRead = 0,
  .radioStateWrite = 0,
  .radioAddressRead = 0,
  .radioAddressWrite = 0,
  .channelRead = 0,
  .channelWrite = 0,
  .destinationRadioAddressRead = 0,
  .destinationRadioAddressWrite = 0,
  .messageLength = 0,
  .messageRead = 0,
  .messageWrite = 0
};

uint8_t currentRegisterNumber;

struct functionMap {
  uint8_t registerNumber;
  void (*handleFunction)(char *myData);
};

void idReturn(char *data);
void firmwareMajorReturn(char *data);
void firmwareMinorReturn(char *data);
void setAddress(char *data);
void getPowerLed(char *data);
void setPowerLed(char *data);
void getRadioState(char *data);
void setRadioState(char *data);
void getRadioAddress(char *data);
void setRadioAddress(char *data);
void getChannel(char *data);
void setChannel(char *data);
void getDestinationRadioAddress(char *data);
void setDestinationRadioAddress(char *data);
void setMessageLength(char *data);
void getMessage(char *data);
void setMessage(char *data);

functionMap functions[] = {
  {registerMap.id, idReturn},
  {registerMap.firmwareMajor, firmwareMajorReturn},
  {registerMap.firmwareMinor, firmwareMinorReturn},
  {registerMap.i2cAddress, setAddress},
  {registerMap.ledRead, getPowerLed},
  {registerMap.ledWrite, setPowerLed},
  {registerMap.radioStateRead, getRadioState},
  {registerMap.radioStateWrite, setRadioState},
  {registerMap.radioAddressRead, getRadioAddress},
  {registerMap.radioAddressWrite, setRadioAddress},
  {registerMap.channelRead, getChannel},
  {registerMap.channelWrite, setChannel},
  {registerMap.destinationRadioAddressRead, getDestinationRadioAddress},
  {registerMap.destinationRadioAddressWrite, setDestinationRadioAddress},
  {registerMap.messageLength, setMessageLength},
  {registerMap.messageRead, getMessage},
  {registerMap.messageWrite, setMessage},
};

typedef struct {
  int           nodeId; //store this nodeId
  char          message[16];
} Payload;
Payload theDataRead;
Payload theDataWrite;

void setup() {
#if DEBUG
  Serial.begin(115200);
  Serial.println("Begin");
#endif
  // Pull up address pins
  pinMode(addressPin1, INPUT_PULLUP);
  pinMode(addressPin2, INPUT_PULLUP);
  pinMode(addressPin3, INPUT_PULLUP);
  pinMode(addressPin4, INPUT_PULLUP);
  pinMode(powerLedPin, OUTPUT);
  powerLed(true); // enable Power LED by default on every power-up
  set_sleep_mode(SLEEP_MODE_IDLE);
  sleep_enable();
  readSystemSettings(); //Load all system settings from EEPROM
  startI2C();          //Determine the I2C address we should be using and begin listening on I2C bus
  oldAddress = valueMap.i2cAddress;

}

void loop() {
  if (updateFlag) {
    startI2C(); // reinitialise I2C with new address, update EEPROM with custom address as necessary
    updateFlag = false;
  }
  if (radio.receiveDone()) {
    debug('[');
    debug(radio.SENDERID);
    debug("] ");
    debug(" [RX_RSSI:");
    debug(radio.readRSSI());
    debug("]");
  }
  // Set up a "buffer" for characters that we'll send:

  static char sendbuffer[62];
  static int sendlength = 0;

  // SENDING

  // In this section, we'll gather serial characters and
  // send them to the other node if we (1) get a carriage return,
  // or (2) the buffer is full (61 characters).

  // If there is any serial input, add it to the buffer:


  //if (Serial.available() > 0)
  if (valueMap.messageLength > 0)
  {
    //debug("(char)valueMap.messageWrite ");
    //debugln((char)valueMap.messageWrite);
    //if (radio.sendWithRetry(valueMap.destinationRadioAddressWrite, valueMap.messageWrite, valueMap.messageLength))
    if (radio.sendWithRetry(valueMap.destinationRadioAddressWrite, "asdf", 4))
      debugln("ACK received!");
    else
      debugln("no ACK received");
    valueMap.messageLength = 0; // Don't resend the same data
    return;
  }

  // RECEIVING

  // In this section, we'll check with the RFM69HCW to see
  // if it has received any packets:

  if (radio.receiveDone()) // Got one!
  {
    // Print out the information:

    debug("received from node ");
    debug(radio.SENDERID);
    debug(", message [");

    // The actual message is contained in the DATA array,
    // and is DATALEN bytes in size:

    for (byte i = 0; i < radio.DATALEN; i++)
      debug((char)radio.DATA[i]);

    // RSSI is the "Receive Signal Strength Indicator",
    // smaller numbers mean higher power.

    debug("], RSSI ");
    debugln(radio.RSSI);

    if (radio.ACKRequested())
    {
      radio.sendACK();
      debugln("ACK sent");
    }
  }
  if (radioState == false) {
    //sleep_mode();  don't use sleep mode until we have everything working
  }
}

// Begin listening on I2C bus as I2C slave using the global variable valueMap.i2cAddress
// ToDo don't use globals ie. pass in value map =>  void startI2C(memoryMap *map)
void startI2C()
{
  uint8_t address;
  uint8_t addressType;
  EEPROM.get(LOCATION_ADDRESS_TYPE, addressType);
  if (addressType == 0xFF) {
    EEPROM.put(LOCATION_ADDRESS_TYPE, SOFTWARE_ADDRESS);
  }

  // Add hardware address jumper values to the default address
  uint8_t IOaddress = DEFAULT_I2C_ADDRESS;
  debug("IOaddress: ");
  debugln(IOaddress);
  uint8_t switchPositions = 0;
  bitWrite(switchPositions, 0, !digitalRead(addressPin1));
  bitWrite(switchPositions, 1, !digitalRead(addressPin2));
  bitWrite(switchPositions, 2, !digitalRead(addressPin3));
  bitWrite(switchPositions, 3, !digitalRead(addressPin4));
  debug("switchPositions: "); debugln(switchPositions);
  debugln(digitalRead(addressPin1));
  if (switchPositions != 0) IOaddress = I2C_ADDRESS_POOL_START + switchPositions; // use the "smart-module address pool" when any hardware address is set

  // If any of the address jumpers are set, we use jumpers
  if ((IOaddress != DEFAULT_I2C_ADDRESS) || (addressType == HARDWARE_ADDRESS))
  {
    debugln("Over-writing Address");
    address = IOaddress;
    EEPROM.put(LOCATION_ADDRESS_TYPE, HARDWARE_ADDRESS);
  }
  // If none of the address jumpers are set, we use registerMap (but check to make sure that the value is legal first)
  else
  {
    debug("valueMap.i2cAddress: "); debugln(valueMap.i2cAddress);
    // if the value is legal, then set it
    if (valueMap.i2cAddress > 0x07 && valueMap.i2cAddress < 0x78)
      address = valueMap.i2cAddress;

    // if the value is illegal, default to the default I2C address for our platform
    else
      address = DEFAULT_I2C_ADDRESS;
  }

  // save new address to the register map
  valueMap.i2cAddress = address;
  debugln("I2C Address:"); debugln(address);
  recordSystemSettings(); // save the new address to EEPROM

  // reconfigure Wire instance
  Wire.end();          //stop I2C on old address
  debug("Address: ");
  debugln(address);
  Wire.begin(address); //rejoin the I2C bus on new address

  // The connections to the interrupts are severed when a Wire.begin occurs, so here we reattach them
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}
