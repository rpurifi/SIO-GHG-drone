# example sensor file for Scripps Institute of Oceanography
# displays sensor readings from HYT939, HP206C, and AMS5915-1000-A

import smbus
import time
import csv

# initializing variables
count=0
modcount=0

# File naming
filename = input("Enter desired file name or hit enter to name with timestamp. ")
if filename == (""): #names file with computer timestamp
	t=time.localtime()
	filename = time.strftime("%Y%m%d %H:%M:%S", t)

print("Your file will be named: ",filename)

# Creating and opening CSV file named with DateTime
with open(filename+'.csv', 'w') as csvfile: 
	filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(["Time", "HP206C_altitude_m", "HYT939_RH_%","HP206C_pressure_mbar","AMS5915_pressure_mbar","HYT939_temp_C","HP206C_temp_C","AMS5915_temp_C"]) #Setting up first row of csv with labels

# While .py file is running, sensors collect data
	while(True):
		# Every 10 lines, print the column labels again
		if modcount == 0:
			print("Time", "HP206C_altitude_m", "HYT939_RH_%","HP206C_pressure_mbar","AMS5915_pressure_mbar","HYT939_temp_C","HP206C_temp_C","AMS5915_temp_C")
			
		# Get I2C bus
		bus = smbus.SMBus(1)
		
		# Recording DateTime
		t=time.localtime()
		current_time = time.strftime("%Y%m%d %H:%M:%S", t)

		# RELATIVE HUMIDITY SENSOR
		# Designated as Sensor #1
		# HYT939 address, 0x28(40)
		#		0x80(128)	Send normal mode
		bus.write_byte(0x28, 0x80)

		time.sleep(0.5)

		# HYT939 address, 0x28(40)
		# Read data back from 0x00(00), 4 bytes
		# Humidity MSB, Humidity LSB, Temp MSB, Temp LSB
		data = bus.read_i2c_block_data(0x28, 0x00, 4)

		# Convert the data to 14-bits
		humidity = ((data[0] & 0x3F) * 256 + data[1]) * (100 / 16383.0)
		cTemp = ((data[2] * 256 + (data[3] & 0xFC)) / 4) * (165 / 16383.0) - 40
		fTemp = cTemp * 1.8 + 32

		# Output data to screen

		hprint="{:.2f}".format(humidity)
		cprint1="{:.2f}".format(cTemp)
		fprint1="{:.2f}".format(fTemp)

		# BAROMETER/ALTIMETER
		# HP206C address, 0x76(118)
		# Send OSR and channel setting command, 0x44(68)
		bus.write_byte(0x76, 0x44 | 0x00)

		time.sleep(0.5)

		# HP206C address, 0x76(118)
		# Read data back from 0x10(16), 6 bytes
		# cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB
		data = bus.read_i2c_block_data(0x76, 0x10, 6)

		# Convert the data to 20-bits
		cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
		fTemp = (cTemp * 1.8) + 32
		pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00

		# HP206C address, 0x76(118)
		# Send OSR and channel setting command, 0x44(68)
		bus.write_byte(0x76, 0x44 | 0x01)

		time.sleep(0.5)

		# HP206C address, 0x76(118)
		# Read data back from 0x31(49), 3 bytes
		# altitude MSB, altitude CSB, altitude LSB
		data = bus.read_i2c_block_data(0x76, 0x31, 3)

		# Convert the data to 20-bits
		altitude = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00

		aprint="{:.2f}".format(altitude)
		pprint2="{:.2f}".format(pressure)
		cprint2="{:.2f}".format(cTemp)
		fprint2="{:.2f}".format(fTemp)
		
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
		
		bus.close()
		
		# Printing all variables as line in terminal
		print (current_time,",", aprint,",", hprint,",",pprint2,",",pprint3,",",cprint1,",",cprint2,",",cprint3)
		# Writing data to csv Files
		filewriter.writerow([current_time, aprint, hprint,pprint2,pprint3,cprint1,cprint2,cprint3])
		
		#increasing count
		count+=1
		modcount=count%10
	
