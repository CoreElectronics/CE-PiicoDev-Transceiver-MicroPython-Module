#include <RFM69.h>
#include <SPI.h>

#define NETWORKID 0  // Must be the same for all nodes
#define MYNODEID 1   // My node ID
#define TONODEID 0   // Destination node ID
#define FREQUENCY RF69_915MHZ
#define ENCRYPTKEY "-PiicoDevRadio- "  // Use the same 16-byte key on all nodes

RFM69 radio;



void setup() {
  // Open a serial port so we can send keystrokes to the module:
  Serial.begin(115200);
  Serial.print("Node ");
  Serial.print(MYNODEID, DEC);
  Serial.println(" ready");

  radio.initialize(FREQUENCY, MYNODEID, NETWORKID);
  radio.setHighPower();
  radio.encrypt(ENCRYPTKEY);
}

int sendNow = 0;
long millisPrev = 0;
uint8_t counter = 0;

void loop() {
  // Set up a "buffer" for characters that we'll send:

  static char sendbuffer[62];
  static int sendlength = 0;


  if ((millis() - millisPrev) > 1000) {
    sendNow = 1;
    millisPrev = millis();
  }
  // SENDING

  // In this section, we'll gather serial characters and
  // send them to the other node if we (1) get a carriage return,
  // or (2) the buffer is full (61 characters).

  // If there is any serial input, add it to the buffer:



  if (sendNow == 1) {
    // Send the packet!

    Serial.print("sending to node ");
    Serial.print(TONODEID, DEC);
    Serial.print(", message [");
    Serial.print(counter);
    Serial.println("]");

    // There are two ways to send packets. If you want
    // acknowledgements, use sendWithRetry():

    // if (radio.sendWithRetry(TONODEID, counter, sendlength))
    //   Serial.println("ACK received!");
    // else
    //   Serial.println("no ACK received");
    radio.send(TONODEID, "1", 1);
    counter++;
    if (counter == 255) {
      counter = 0;
    }
    sendNow = 0;
  }

  // RECEIVING

  // In this section, we'll check with the RFM69HCW to see
  // if it has received any packets:

  if (radio.receiveDone())  // Got one!
  {
    // Print out the information:

    Serial.print("received from node ");
    Serial.print(radio.SENDERID, DEC);
    Serial.print(", message [");

    // The actual message is contained in the DATA array,
    // and is DATALEN bytes in size:

    for (byte i = 0; i < radio.DATALEN; i++)
      Serial.print((char)radio.DATA[i]);

    // RSSI is the "Receive Signal Strength Indicator",
    // smaller numbers mean higher power.

    Serial.print("], RSSI ");
    Serial.println(radio.RSSI);

    if (radio.ACKRequested()) {
      radio.sendACK();
      Serial.println("ACK sent");
    }
  }
}