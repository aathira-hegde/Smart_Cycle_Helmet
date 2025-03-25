file: blePeripheral.py
Usage: UPLOAD TO ESP32

Function:  __init__
Usage:     initializes BLE class
To update: self.timer is the interrupt being used to call send data. This will be changed to the IMU interrupt
	       self.name to whatever name you want to have, ensure constant in PC file matches
		   self.ble.config(mtu=324), change for however many bytes are able to be sent to PC at once

Function:  send_data
Usage:     Sends data to the PC if there is a valid connect
To update: self.counter to be the actual tuple of data wea are using
To update: data = struct.pack('156h', *simulate_payload), change 156h however many bytes to send to PC

-------------------------------------------------------------------------

file: BleMultiDevice.py
Usage: RUN ON WINDOWS COMPUTER

Function:  send_data
Usage:     Sends data to the PC if there is a valid connect
To update: replace with actual data from the sensor


Function: recieve_data
Usage: Reads data in from ESP32
To update: value = struct.unpack('156h', data), change156h to whatever value you are sending on ESP32