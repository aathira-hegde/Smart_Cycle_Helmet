import machine
from machine import Pin, I2C
from time import sleep
import time
import struct

LSM6DSOX_ADDR = 0x6A 
WHO_AM_I_REG = 0x0F
WAKE_UP_THS  = 0x5B
WAKE_UP_DUR = 0x5C
MD1_CFG = 0x5E
FIFO_CTRL4 = 0x0A
CTRL1_XL =0x10
CTRL2_G  = 0x11
CTRL3_C = 0x12
FIFO_CTRL1 = 0x07
FIFO_CTRL2 = 0x08
FIFO_CTRL3 = 0x09
INT1_CTRL = 0x0D
INT2_CTRL  = 0x0E
FREE_FALL = 0x5D
WAKE_UP_SRC  = 0x1B

FIFO_STATUS1 = 0x3A
FIFO_STATUS2 = 0x3B
FIFO_DATA_OUT_L = 0x78
FIFO_DATA_OUT_H = 0x79

OUTX_AXL = 0x28
OUTY_AXL = 0x2A
OUTZ_AXL = 0x2C

NEOI2C_PWR = Pin(2, Pin.OUT)
NEOI2C_PWR.value(0)
sleep(0.5)
NEOI2C_PWR.value(1)
i2c = I2C(0, scl=Pin(20), sda=Pin(22), freq=400000)

def read_fifo_status():
    status1 = i2c.readfrom_mem(LSM6DSOX_ADDR, FIFO_STATUS1, 1)[0]
    status2 = i2c.readfrom_mem(LSM6DSOX_ADDR, FIFO_STATUS2, 1)[0]
    fifo_level = status1 | ((status2 & 0x03) << 8)  # FIFO level (10-bit)
    fifo_full = (status2 & 0x20) != 0
    return fifo_level, fifo_full

def read_fifo_data(FIFO_Size):
    data = []
    while(FIFO_Size>0):
        raw_data = read_register(FIFO_DATA_OUT_H, 12)
        ax, ay, az, gx, gy, gz = struct.unpack('<hhhhhh', raw_data)
        #print(f"Accel: {ax}, {ay}, {az} | Gyro: {gx}, {gy}, {gz}")
        data.append(raw_data)
        FIFO_Size = FIFO_Size - 1
    return data


def read_device_id():
    try:
        device_id = i2c.readfrom_mem(LSM6DSOX_ADDR, WHO_AM_I_REG, 1)
        print("LSM6DSOX ID:", hex(device_id[0]))
    except OSError:
        print("Failed to communicate with LSM6DSOX. Check connections.")
def read_register(register, _count):
    i2c_data = []
    try:
        i2c_data = i2c.readfrom_mem(LSM6DSOX_ADDR, register, _count)
    except OSError:
        print("Failed to read from register.")
    return i2c_data
    
def write_register(register, value):
    try:
        i2c.writeto_mem(LSM6DSOX_ADDR, register, bytes([value]))
        print(f"Wrote {hex(value)} to register {hex(register)}")
    except OSError:
        print("Failed to write to register. Check connections.")
def bytes_to_int16(msb, lsb):
    """Convert two bytes (MSB and LSB) to a signed 16-bit integer."""
    value = (msb << 8) | lsb  # Combine bytes
    if value & 0x8000:  # Check if the sign bit (15th bit) is set
        value -= 0x10000  # Convert to negative value
    return value

# Run the function
device_id = read_register(WHO_AM_I_REG,1)
if(len(device_id)>0):
    print("LSM6DSOX ID:", hex(device_id[0]))
else:
    print("Failed to communicate with LSM6DSOX. Check connections.")

INT1 = Pin(13, Pin.IN)
write_register(WAKE_UP_THS, 0x02)
write_register(WAKE_UP_DUR, 0x02)
write_register(CTRL3_C, 0x04)
write_register(MD1_CFG, 0b00000010)
write_register(FIFO_CTRL4,0x06)


write_register(FIFO_CTRL1, 54)
write_register(FIFO_CTRL2, 0b00000000)
write_register(INT1_CTRL, 0b00001000)
write_register(FIFO_CTRL3, 0x22)

write_register(FREE_FALL, 0b00001100)
write_register(CTRL1_XL, 0b00100100)
write_register(CTRL2_G , 0b00101100)

ACCEL_SENSITIVITY = 0.000488 *9.81  # g/LSB for ±16g
while(1):
    if(INT1.value()==1):
        fifo_level, fifo_full = read_fifo_status()
        print("fifo_level=" + str(fifo_level))
        if(fifo_level>0):
            read_fifo_data(fifo_level)
            #AXL_Data = read_register(OUTX_AXL,6)
            #AXL_X = bytes_to_int16(AXL_Data[1], AXL_Data[0])
            #AXL_Y = bytes_to_int16(AXL_Data[3],AXL_Data[2])
            #AXL_Z = bytes_to_int16(AXL_Data[5], AXL_Data[4])
            #print("AXL data = ", AXL_X * ACCEL_SENSITIVITY,AXL_Y * ACCEL_SENSITIVITY,AXL_Z  * ACCEL_SENSITIVITY)
    #sleep(5.2)




