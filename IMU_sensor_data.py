##This Code is still a work in progress, output is not perfect.

##Currently the code detects the IMU device and scans for motion. 
##If no motion is detected for 30 seconds after running the code the microcontroller will go into an idle mode where it will scan every 10 seconds, if motion is detected within the 10 second time frame the microcontroller will go back into an "awake mode" and scan every second until there is no motion for 30 seconds.

import machine
from machine import Pin, I2C
from time import sleep
import time
import struct

LSM6DSOX_ADDR = 0x6A
WHO_AM_I_REG = 0x0F
WAKE_UP_THS = 0x5B
WAKE_UP_DUR = 0x5C
MD1_CFG = 0x5E
FIFO_CTRL1 = 0x07
FIFO_CTRL2 = 0x08
FIFO_CTRL3 = 0x09
FIFO_CTRL4 = 0x0A
INT1_CTRL = 0x0D
FREE_FALL = 0x5D
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
FIFO_STATUS1 = 0x3A
FIFO_STATUS2 = 0x3B
FIFO_DATA_OUT_L = 0x78
FIFO_DATA_OUT_H = 0x79
OUTX_AXL = 0x28

# Power cycle the I2C device
NEOI2C_PWR = Pin(2, Pin.OUT)
NEOI2C_PWR.value(0)
sleep(0.5)
NEOI2C_PWR.value(1)
i2c = I2C(0, scl=Pin(20), sda=Pin(22), freq=400000)

def read_register(register, _count):
    try:
        return i2c.readfrom_mem(LSM6DSOX_ADDR, register, _count)
    except OSError:
        print(f"Failed to read from register: {hex(register)}")
        return None

def write_register(register, value):
    try:
        i2c.writeto_mem(LSM6DSOX_ADDR, register, bytes([value]))
        print(f"Wrote {hex(value)} to register {hex(register)}")
    except OSError:
        print("Failed to write to register. Check connections.")

def bytes_to_int16(msb, lsb):
    value = (msb << 8) | lsb
    if value & 0x8000:
        value -= 0x10000
    return value

def read_fifo_status():
    status1 = read_register(FIFO_STATUS1, 1)[0]
    status2 = read_register(FIFO_STATUS2, 1)[0]
    fifo_level = status1 | ((status2 & 0x03) << 8)  # FIFO level (10-bit)
    fifo_full = (status2 & 0x20) != 0
    return fifo_level, fifo_full

def read_fifo_data(FIFO_Size):
    data = []
    while FIFO_Size > 0:
        raw_data = read_register(FIFO_DATA_OUT_H, 12)
        ax, ay, az, gx, gy, gz = struct.unpack('<hhhhhh', raw_data)
        print(f"Accel: {ax}, {ay}, {az} | Gyro: {gx}, {gy}, {gz}")
        data.append(raw_data)
        FIFO_Size -= 1
    return data

def enter_idle_mode():
    print("Entering idle mode...")
    write_register(CTRL1_XL, 0x20)  # Set accelerometer ODR to 26 Hz, 2g
    write_register(CTRL2_G, 0x20)  # Set gyroscope ODR to 26 Hz, 2000 dps

def exit_idle_mode():
    print("Exiting idle mode...")
    write_register(CTRL1_XL, 0x20)  # Set accelerometer ODR to 26 Hz, 2g
    write_register(CTRL2_G, 0x20)  # Set gyroscope ODR to 26 Hz, 2000 dps

# Check communication with the sensor
device_id = read_register(WHO_AM_I_REG, 1)
if device_id is None or len(device_id) == 0 or device_id[0] != 0x6C:
    print("Failed to communicate with LSM6DSOX. Check connections.")
else:
    print("LSM6DSOX sensor found. WHO_AM_I:", hex(device_id[0]))

    # Initialization
    write_register(CTRL3_C, 0x44)  # Enable Block Data Update and auto-increment
    write_register(CTRL1_XL, 0x20)  # Set accelerometer ODR to 26 Hz, 2g
    write_register(CTRL2_G, 0x20)  # Set gyroscope ODR to 26 Hz, 2000 dps
    write_register(WAKE_UP_THS, 0x02)
    write_register(WAKE_UP_DUR, 0x02)
    write_register(MD1_CFG, 0b00000010)
    write_register(FIFO_CTRL1, 0x20)  # Set watermark level to 32 (FIFO threshold)
    write_register(FIFO_CTRL2, 0b00001100)  # Set FIFO mode to continuous mode
    write_register(FIFO_CTRL3, 0x22)  # Enable FIFO for accelerometer data
    write_register(FIFO_CTRL4, 0x06)
    write_register(INT1_CTRL, 0b00000111)
    write_register(FREE_FALL, 0b00001100)

    print("Waiting for motion...")

    previous_AXL_X = 0
    previous_AXL_Y = 0
    previous_AXL_Z = 0
    threshold_initial = 10000  # Higher initial threshold to reduce false positives
    threshold_normal = 5000  # Normal threshold for motion detection
    threshold = threshold_initial
    debounce_time = 2  # Number of seconds to debounce motion detection
    last_motion_time = 0
    stabilization_time = 5  # Time to wait before switching to normal threshold
    idle_time = 30  # Time to wait before entering idle mode
    idle_scan_interval = 10  # Idle mode scan interval

    start_time = time.time()
    stabilized = False
    idle_mode = False

    while True:
        if idle_mode:
            sleep(idle_scan_interval)
            exit_idle_mode()
            idle_mode = False
            start_time = time.time()  # Reset the timer
            continue

        fifo_level, fifo_full = read_fifo_status()
        print("fifo_level = " + str(fifo_level))
        if fifo_level > 0:
            read_fifo_data(fifo_level)
            AXL_Data = read_register(OUTX_AXL, 6)
            if AXL_Data:
                AXL_X = bytes_to_int16(AXL_Data[1], AXL_Data[0])
                AXL_Y = bytes_to_int16(AXL_Data[3], AXL_Data[2])
                AXL_Z = bytes_to_int16(AXL_Data[5], AXL_Data[4])
                print("AXL data = ", AXL_X, AXL_Y, AXL_Z)

                # Detect motion by comparing current and previous values
                current_time = time.time()
                if ((abs(AXL_X - previous_AXL_X) > threshold or
                     abs(AXL_Y - previous_AXL_Y) > threshold or
                     abs(AXL_Z - previous_AXL_Z) > threshold) and
                    (current_time - last_motion_time > debounce_time)):
                    print("Motion detected!")
                    last_motion_time = current_time

                # Update previous values
                previous_AXL_X = AXL_X
                previous_AXL_Y = AXL_Y
                previous_AXL_Z = AXL_Z

                # Switch to normal threshold after stabilization time
                if not stabilized and (current_time - start_time > stabilization_time):
                    threshold = threshold_normal
                    stabilized = True

                # Enter idle mode if no motion is detected for idle_time seconds
                if current_time - last_motion_time > idle_time:
                    enter_idle_mode()
                    idle_mode = True

        sleep(1 if not idle_mode else idle_scan_interval)
