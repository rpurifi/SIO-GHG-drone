# This code is designed to work with the AMS5915-1000-A pressure sensor.
# Modified from https://github.com/ControlEverythingCommunity/AMS5915_0100_D/blob/7f3538a1c179cb82f54dd60ec26c6b148136eb5a/Python/AMS5915_0100_D.py

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# AMS5915-1000-A

# AMS5915_0100_A address, 0x28(40)
# Read data back, 4 bytes
# pres MSB, pres LSB, temp MSB, temp LSB
data = bus.read_i2c_block_data(0x28, 4)

# Convert the data
pres = ((data[0] & 0x3F) * 256) + data[1]
temp = ((data[2] * 256) + (data[3] & 0xE0)) / 32
pressure = (pres - 1638.0) / (13107.0 / 1000.0)
cTemp = ((temp * 200.0) / 2048) - 50.0
fTemp = (cTemp * 1.8 ) + 32

# Output data to screen
pprint3="{:.2f}".format(pressure)
cprint3="{:.2f}".format(cTemp)
fprint3="{:.2f}".format(fTemp)

print (pprint3)
print (cprint3)
print (fprint3)

