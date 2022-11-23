/*
   PiicoDev Radio Firmware
   Written by Peter Johnston @ Core Electronics
   Based off the Core Electronics Potentiometer module https://github.com/CoreElectronics/CE-PiicoDev-Potentiometer-MicroPython-Module
   Based off work by Felix Rusu 2018, http://www.LowPowerLab.com/contact
   Date: OCTOBER 2022
   An I2C based module that utilises an RFM69 radio

   Feel like supporting PiicoDev? Buy a module here:
   Radio: https://core-electronics.com.au/catalog/product/view/sku/CE08757

*/

#include <RFM69.h> // by LowPowerLab version 1.5.2 get it here: https://www.github.com/lowpowerlab/rfm69
//#include <RFM69_ATC.h>     //get it here: https://www.github.com/lowpowerlab/rfm69
//#include <SPIFlash.h>      //get it here: https://www.github.com/lowpowerlab/spiflash
#include <SPI.h>  //included with Arduino IDE install (www.arduino.cc)
#include <RFM69registers.h>
#include <CircularBuffer.h> // by AgileWare version 1.3.3
#include <SoftwareSerial.h>

#define DEBUG false // If true, expect I2C bus to hang for 1s for I2C transactions
#if DEBUG == true
#define debug(x) swsri.print(x)
#define debugln(x) swsri.println(x)
#else
#define debug(x)
#define debugln(x)
#endif

#include <Wire.h>
#include <EEPROM.h>
#include <stdint.h>

#define FIRMWARE_MAJOR 0x01
#define FIRMWARE_MINOR 0x00
#define DEVICE_ID 495
#define DEFAULT_I2C_ADDRESS 0x1A     // The default address when all switches are off
#define I2C_ADDRESS_POOL_START 0x08  // The start of the 'smart module address pool' minus 1 - addresses settable by switches
#define SOFTWARE_ADDRESS true
#define HARDWARE_ADDRESS false
#define I2C_BUFFER_SIZE 32  //For ATmega328 based Arduinos, the I2C buffer is limited to 32 bytes
#define RX_BUFFER_SIZE 64
#define FREQUENCY RF69_915MHZ
//#define FREQUENCY   RF69_433MHZ
#define MYNODEID 1
#define NETWORKID 0
#define TONODEID 0
#define SERIAL_RX_PIN 6
#define SERIAL_TX_PIN 7

RFM69 radio;
CircularBuffer<byte, RX_BUFFER_SIZE> payloadBufferIncoming;
CircularBuffer<byte, RX_BUFFER_SIZE> payloadBufferOutgoing;
SoftwareSerial swsri(SERIAL_RX_PIN, SERIAL_TX_PIN);

enum eepromLocations {
  LOCATION_I2C_ADDRESS = 0x00,   // Device's address
  LOCATION_ADDRESS_TYPE = 0x01,  // Address type can be either hardware defined (jumpers/switches), or software defined by user.
};

uint8_t oldAddress;

// Hardware Connectins
// Prototyping with Arduino Uno
#if defined(__AVR_ATmega328P__)
const uint8_t powerLedPin = 3;
const uint16_t addressPin1 = 8;
const uint16_t addressPin2 = 7;
const uint16_t addressPin3 = 6;
const uint16_t addressPin4 = 4;
#else
// ATTINY 8x6 or 16x6
const uint8_t powerLedPin = PIN_PA5;
const uint8_t addressPin1 = PIN_PC3;
const uint8_t addressPin2 = PIN_PC2;
const uint8_t addressPin3 = PIN_PC1;
const uint8_t addressPin4 = PIN_PC0;

#endif

// System global variables
volatile bool updateFlag = true;  // Goes true when new data received
volatile uint32_t lastSyncTime = 0;

#define LOCAL_BUFFER_SIZE 32              // bytes
uint8_t incomingData[LOCAL_BUFFER_SIZE];  // Local buffer to record I2C bytes
volatile uint16_t incomingDataSpot = 0;   // Keeps track of where we are in the incoming buffer

uint8_t responseBuffer[I2C_BUFFER_SIZE];  // Used to pass data back to master
volatile uint8_t responseSize = 1;        // Defines how many bytes of relevant data is contained in the responseBuffer

bool radioState = true;

struct memoryMapRegs {
  uint8_t id;
  uint8_t firmwareMajor;
  uint8_t firmwareMinor;
  uint8_t i2cAddress;
  uint8_t ledRead;
  uint8_t ledWrite;
  uint8_t highPowerRead;
  uint8_t highPowerWrite;
  uint8_t rfm69RadioStateRead;
  uint8_t rfm69RadioStateWrite;
  uint8_t rfm69NodeIDRead;
  uint8_t rfm69NodeIDWrite;
  uint8_t rfm69NetworkIDRead;
  uint8_t rfm69NetworkIDWrite;
  uint8_t rfm69ToNodeIDRead;
  uint8_t rfm69ToNodeIDWrite;
  uint8_t rfm69Reg;
  uint8_t rfm69ValueRead;
  uint8_t rfm69ValueWrite;
  uint8_t payloadLengthRead;
  uint8_t payloadLengthWrite;
  uint8_t payloadRead;
  uint8_t payloadWrite;
  uint8_t payloadNew;
  uint8_t payloadGo;
};

struct memoryMapData {
  uint16_t id;
  uint8_t firmwareMajor;
  uint8_t firmwareMinor;
  uint8_t i2cAddress;
  uint8_t ledRead;
  uint8_t ledWrite;
  uint8_t highPowerRead;
  uint8_t highPowerWrite;
  uint8_t rfm69RadioStateRead;
  uint8_t rfm69RadioStateWrite;
  uint8_t rfm69NodeIDRead;
  uint8_t rfm69NodeIDWrite;
  uint8_t rfm69NetworkIDRead;
  uint8_t rfm69NetworkIDWrite;
  uint8_t rfm69ToNodeIDRead;
  uint8_t rfm69ToNodeIDWrite;
  uint8_t rfm69Reg;
  uint8_t rfm69ValueRead;
  uint8_t rfm69ValueWrite;
  uint8_t payloadLengthRead;
  uint8_t payloadLengthWrite;
  uint8_t payloadRead;  // Dummy - CircularBuffer payloadBufferIncoming used instead
  uint8_t payloadWrite; // Dummy - CircularBuffer payloadBufferOutgoing used instead
  uint8_t payloadNew;
  uint8_t payloadGo;
};

// Register addresses.
const memoryMapRegs registerMap = {
  .id = 0x01,
  .firmwareMajor = 0x02,
  .firmwareMinor = 0x03,
  .i2cAddress = 0x84,
  .ledRead = 0x05,
  .ledWrite = 0x85,
  .highPowerRead = 0x13,
  .highPowerWrite = 0x93,
  .rfm69RadioStateRead = 0x14,
  .rfm69RadioStateWrite = 0x94,
  .rfm69NodeIDRead = 0x15,
  .rfm69NodeIDWrite = 0x95,
  .rfm69NetworkIDRead = 0x16,
  .rfm69NetworkIDWrite = 0x96,
  .rfm69ToNodeIDRead = 0x17,
  .rfm69ToNodeIDWrite = 0x97,
  .rfm69Reg = 0x98,
  .rfm69ValueRead = 0x19,
  .rfm69ValueWrite = 0x99,
  .payloadLengthRead = 0x21,
  .payloadLengthWrite = 0xA1,
  .payloadRead = 0x22,
  .payloadWrite = 0xA2,
  .payloadNew = 0x23,
  .payloadGo = 0xA4,
};

volatile memoryMapData valueMap = {
  .id = DEVICE_ID,
  .firmwareMajor = FIRMWARE_MAJOR,
  .firmwareMinor = FIRMWARE_MINOR,
  .i2cAddress = DEFAULT_I2C_ADDRESS,
  .ledRead = 1,
  .ledWrite = 1,
  .highPowerRead = 0,
  .highPowerWrite = 0,
  .rfm69RadioStateRead = 0,
  .rfm69RadioStateWrite = 0,
  .rfm69NodeIDRead = 1,
  .rfm69NodeIDWrite = 1,
  .rfm69NetworkIDRead = 0,
  .rfm69NetworkIDWrite = 0,
  .rfm69ToNodeIDRead = 0,
  .rfm69ToNodeIDWrite = 0,
  .rfm69Reg = 0,
  .rfm69ValueRead = 0,
  .rfm69ValueWrite = 0,
  .payloadLengthRead = 0,
  .payloadLengthWrite = 0,
  .payloadRead = 0,
  .payloadWrite = 0,
  .payloadNew = 0,
  .payloadGo = 0,
};

uint8_t currentRegisterNumber;

struct functionMap {
  uint8_t registerNumber;
  void (*handleFunction)(int numberOfBytesReceived, char *myData);
};

void idReturn(int numberOfBytesReceived, char *data);
void firmwareMajorReturn(int numberOfBytesReceived, char *data);
void firmwareMinorReturn(int numberOfBytesReceived, char *data);
void setAddress(int numberOfBytesReceived, char *data);
void getPowerLed(int numberOfBytesReceived, char *data);
void setPowerLed(int numberOfBytesReceived, char *data);
void getHighPower(int numberOfBytesReceived, char *data);
void setHighPower(int numberOfBytesReceived, char *data);
void getRfm69RadioState(int numberOfBytesReceived, char *data);
void setRfm69RadioState(int numberOfBytesReceived, char *data);
void getRfm69NodeID(int numberOfBytesReceived, char *data);
void setRfm69NodeID(int numberOfBytesReceived, char *data);
void getRfm69NetworkID(int numberOfBytesReceived, char *data);
void setRfm69NetworkID(int numberOfBytesReceived, char *data);
void getRfm69ToNodeID(int numberOfBytesReceived, char *data);
void setRfm69ToNodeID(int numberOfBytesReceived, char *data);
void setRfm69Reg(int numberOfBytesReceived, char *data);
void getRfm69Value(int numberOfBytesReceived, char *data);
void setRfm69Value(int numberOfBytesReceived, char *data);
void receivePayloadLength(int numberOfBytesReceived, char *data);
void sendPayloadLength(int numberOfBytesReceived, char *data);
void receivePayload(int numberOfBytesReceived, char *data);
void sendPayload(int numberOfBytesReceived, char *data);
void receivePayloadNew(int numberOfBytesReceived, char *data);
void sendPayloadGo(int numberOfBytesReceived, char *data);

functionMap functions[] = {
  { registerMap.id, idReturn },
  { registerMap.firmwareMajor, firmwareMajorReturn },
  { registerMap.firmwareMinor, firmwareMinorReturn },
  { registerMap.i2cAddress, setAddress },
  { registerMap.ledRead, getPowerLed },
  { registerMap.ledWrite, setPowerLed },
  { registerMap.highPowerRead, getHighPower },
  { registerMap.highPowerWrite, setHighPower },
  { registerMap.rfm69RadioStateRead, getRfm69RadioState },
  { registerMap.rfm69RadioStateWrite, setRfm69RadioState },
  { registerMap.rfm69NodeIDRead, getRfm69NodeID },
  { registerMap.rfm69NodeIDWrite, setRfm69NodeID },
  { registerMap.rfm69NetworkIDRead, getRfm69NetworkID },
  { registerMap.rfm69NetworkIDWrite, setRfm69NetworkID },
  { registerMap.rfm69ToNodeIDRead, getRfm69ToNodeID },
  { registerMap.rfm69ToNodeIDWrite, setRfm69ToNodeID },
  { registerMap.rfm69Reg, setRfm69Reg },
  { registerMap.rfm69ValueRead, getRfm69Value },
  { registerMap.rfm69ValueWrite, setRfm69Value },
  { registerMap.payloadLengthRead, receivePayloadLength },
  { registerMap.payloadLengthWrite, sendPayloadLength },
  { registerMap.payloadRead, receivePayload },
  { registerMap.payloadWrite, sendPayload },
  { registerMap.payloadNew, receivePayloadNew },
  { registerMap.payloadGo, sendPayloadGo },
};

typedef struct {
  int nodeId;  //store this nodeId
  char message[16];
} Payload;
Payload theDataRead;
Payload theDataWrite;

void setup() {
#if DEBUG
  swsri.begin(9600);
  Serial.println("Begin");
#endif
  // Pull up address pins
  pinMode(addressPin1, INPUT_PULLUP);
  pinMode(addressPin2, INPUT_PULLUP);
  pinMode(addressPin3, INPUT_PULLUP);
  pinMode(addressPin4, INPUT_PULLUP);
  pinMode(powerLedPin, OUTPUT);
  powerLed(true);  // enable Power LED by default on every power-up
  // Open a serial port so we can send keystrokes to the module:
  debug("Node ");
  debug(MYNODEID);
  debugln(" ready");

  readSystemSettings();  //Load all system settings from EEPROM
  startI2C();            //Determine the I2C address we should be using and begin listening on I2C bus
  oldAddress = valueMap.i2cAddress;

  radio.initialize(FREQUENCY, valueMap.rfm69NodeIDWrite, valueMap.rfm69NetworkIDWrite);
  radio.setHighPower(true);
  radio.writeReg(REG_OPMODE, RF_OPMODE_SEQUENCER_ON | RF_OPMODE_LISTEN_OFF | RF_OPMODE_STANDBY);
  radio.writeReg(REG_DATAMODUL, RF_DATAMODUL_DATAMODE_PACKET | RF_DATAMODUL_MODULATIONTYPE_FSK | RF_DATAMODUL_MODULATIONSHAPING_00);                                        // 0x02
  radio.writeReg(REG_BITRATEMSB, RF_BITRATEMSB_300000);                                                                                                                     // 0x03
  radio.writeReg(REG_BITRATELSB, RF_BITRATELSB_300000);                                                                                                                     // 0x04
  radio.writeReg(REG_FDEVMSB, RF_FDEVMSB_300000);                                                                                                                           // 0x05
  radio.writeReg(REG_FDEVLSB, RF_FDEVLSB_300000);                                                                                                                           // 0x06
  radio.writeReg(REG_FRFMSB, RF_FRFMSB_915);                                                                                                                                // 0x07
  radio.writeReg(REG_FRFMID, RF_FRFMID_915);                                                                                                                                // 0x08
  radio.writeReg(REG_FRFLSB, RF_FRFLSB_915);                                                                                                                                // 0x09
  radio.writeReg(REG_RXBW, RF_RXBW_DCCFREQ_111 | RF_RXBW_MANT_16 | RF_RXBW_EXP_0);                                                                                          // 0x19
  radio.writeReg(REG_DIOMAPPING1, RF_DIOMAPPING1_DIO0_01);                                                                                                                  // 0x25
  radio.writeReg(REG_DIOMAPPING2, RF_DIOMAPPING2_CLKOUT_OFF);                                                                                                               //0x26
  radio.writeReg(REG_IRQFLAGS2, RF_IRQFLAGS2_FIFOOVERRUN);                                                                                                                  // 0x28
  radio.writeReg(REG_RSSITHRESH, 220);                                                                                                                                      // 0x29
  radio.writeReg(REG_PREAMBLELSB, 6);                                                                                                                                       // 0x2D
  radio.writeReg(REG_SYNCCONFIG, RF_SYNC_ON | RF_SYNC_FIFOFILL_AUTO | RF_SYNC_SIZE_3 | RF_SYNC_TOL_0);                                                                      // 0x2E
  radio.writeReg(REG_SYNCVALUE1, 0x88);                                                                                                                                     // 0x2F
  radio.writeReg(REG_SYNCVALUE2, NETWORKID);                                                                                                                                // 0x30
  radio.writeReg(REG_SYNCVALUE3, 0x88);                                                                                                                                     // 0x2F
  radio.writeReg(REG_PACKETCONFIG1, RF_PACKET1_FORMAT_VARIABLE | RF_PACKET1_DCFREE_OFF | RF_PACKET1_CRC_OFF | RF_PACKET1_CRCAUTOCLEAR_OFF | RF_PACKET1_ADRSFILTERING_OFF);  // 0x37
  radio.writeReg(REG_PAYLOADLENGTH, 66);                                                                                                                                    // 0x38
  radio.writeReg(REG_FIFOTHRESH, RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY | RF_FIFOTHRESH_VALUE);                                                                                 // 0x3C
  radio.writeReg(REG_PACKETCONFIG2, RF_PACKET2_RXRESTARTDELAY_2BITS | RF_PACKET2_AUTORXRESTART_ON | RF_PACKET2_AES_OFF);                                                    // 0x3D
  radio.writeReg(REG_TESTDAGC, RF_DAGC_IMPROVED_LOWBETA0);                                                                                                                  // 0x6F

  //radio.setPowerLevel(0);
  radio.encrypt(null);
}

uint8_t counter = 0;
long millisPrev = 0;

char *payloadRead;
char *payloadWrite;
uint8_t rfm69ToNodeIDWrite = 0;
uint8_t payloadLengthWrite;
uint8_t payloadGo = 0;
uint8_t payloadNew = 0;
uint8_t payloadLengthRead = 0;
int sendNow = 0;


void loop() {
  if (updateFlag) {
    startI2C();  // reinitialise I2C with new address, update EEPROM with custom address as necessary
    updateFlag = false;
  }

  if (valueMap.payloadGo > 0) {
    // Send the packet!
    uint8_t transmitBuffer[RX_BUFFER_SIZE];
    for (byte i = 0; i < RX_BUFFER_SIZE; i++) {
      transmitBuffer[i] = 0;
    }

    debug("sending to node ");
    debug(TONODEID);
    debug(", message [");
    debug(counter);
    debugln("]");
    uint8_t i = 0;
    while (!payloadBufferOutgoing.isEmpty()) {
      transmitBuffer[i] = payloadBufferOutgoing.shift();
      debug((char)transmitBuffer[i]);
      i++;
    }
    radio.send(valueMap.rfm69ToNodeIDWrite, transmitBuffer, valueMap.payloadLengthWrite);  //radio.send(valueMap.rfm69ToNodeIDWrite, valueMap.payloadWrite, valueMap.payloadLengthWrite);
    debugln("sent");
    counter++;
    if (counter == 255) {
      counter = 0;
    }
    payloadBufferOutgoing.clear();
    valueMap.payloadGo = 0;
  }

  // RECEIVING

  // In this section, we'll check with the RFM69HCW to see
  // if it has received any packets:

  if (radio.receiveDone())  // Got one
  {
    // Print out the information:
    debugln(F("-------------------"));
    debug(F("received from node "));
    debug(radio.SENDERID);
    debug(F(", message ["));

    valueMap.payloadNew = 1;
    payloadBufferIncoming.clear();
    payloadBufferIncoming.push(abs(radio.RSSI));
    for (byte i = 0; i < radio.DATALEN; i++) {
      debug((char)radio.DATA[i]);
      payloadBufferIncoming.push((char)radio.DATA[i]);
      debug("");
    }
    debug(F("]"));
    valueMap.payloadLengthRead = radio.DATALEN;
    debug("PayloadLengthRead:");
    debug(valueMap.payloadLengthRead);
    debug(" RSSI:");
    debugln(radio.RSSI);
  }
}

// Begin listening on I2C bus as I2C target using the global variable valueMap.i2cAddress
void startI2C() {
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
  debug("switchPositions: ");
  debugln(switchPositions);
  debugln(digitalRead(addressPin1));
  if (switchPositions != 0) IOaddress = I2C_ADDRESS_POOL_START + switchPositions;  // use the "smart-module address pool" when any hardware address is set

  // If any of the address jumpers are set, we use jumpers
  if ((IOaddress != DEFAULT_I2C_ADDRESS) || (addressType == HARDWARE_ADDRESS)) {
    debugln("Over-writing Address");
    address = IOaddress;
    EEPROM.put(LOCATION_ADDRESS_TYPE, HARDWARE_ADDRESS);
  }
  // If none of the address jumpers are set, we use registerMap (but check to make sure that the value is legal first)
  else {
    debug("valueMap.i2cAddress: ");
    debugln(valueMap.i2cAddress);
    // if the value is legal, then set it
    if (valueMap.i2cAddress > 0x07 && valueMap.i2cAddress < 0x78)
      address = valueMap.i2cAddress;

    // if the value is illegal, default to the default I2C address for our platform
    else
      address = DEFAULT_I2C_ADDRESS;
  }

  // save new address to the register map
  valueMap.i2cAddress = address;
  //debugln("I2C Address:"); debugln(address);
  recordSystemSettings();  // save the new address to EEPROM

  // reconfigure Wire instance
  Wire.end();  //stop I2C on old address
  //debug("Address: ");
  //debugln(address);
  Wire.begin(address);  //rejoin the I2C bus on new address

  // The connections to the interrupts are severed when a Wire.begin occurs, so here we reattach them
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}
