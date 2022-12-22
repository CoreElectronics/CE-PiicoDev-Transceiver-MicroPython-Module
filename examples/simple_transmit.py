from PiicoDev_Transceiver import PiicoDev_Transceiver
from PiicoDev_Unified import sleep_ms

radio = PiicoDev_Transceiver()

# Example: Send a string
radio.send("Hello, World!")

# Example: Send a value with a name
radio.send("my_integer", 256)
radio.send("my_float", 123.456)