from machine import I2C, Pin


# Define register addresses
LSM6DSOX_ADDR	= 	0x6A
FIFO_CTRL1 		= 	0x07
FIFO_CTRL2 		= 	0x08
FIFO_CTRL3 		= 	0x09
FIFO_CTRL4 		= 	0x0A
INT1_CTRL 		= 	0x0D
INT2_CTRL 		= 	0x0E
WHO_AM_I_REG 	= 	0x0F
CTRL1_XL 		= 	0x10
CTRL2_G 		= 	0x11
CTRL3_C			= 	0x12
CTRL10_C		=	0x19
WAKE_UP_SRC 	= 	0x1B
TAP_SRC			=	0x1C
FIFO_STATUS1	=	0x3A
FIFO_STATUS2	=	0x3B
WAKE_UP_THS		= 	0x5B
WAKE_UP_DUR		=	0x5C
FREE_FALL		=	0x5D
MD1_CFG			=	0x5E
MD2_CFG			=	0x5F
FIFO_DO_TAG		=	0x78
FIFO_DO_XL		=  	0x79
FIFO_DO_XH		=	0x7A
FIFO_DO_YL		=  	0x7B
FIFO_DO_YH		=	0x7C
FIFO_DO_ZL		=  	0x7D
FIFO_DO_ZH		=	0x7E
FIFO_TAP_CFG0	=	0x56
TAP_CFG2		=	0x58

# NEOI2C_PWR = Pin(2, Pin.OUT)
# NEOI2C_PWR.value(0)
# sleep(0.5)
# NEOI2C_PWR.value(1)
# Currently, using 3.3V Pin to power the sensor

# Set the fifo_threshold interrupt
int1_cfg		=	const(0b00001000)

# No other interrupts set
md2_cfg			= 	const(0b00000000)
md1_cfg			=	const(0b00000000)




class Adafruit_LSM6DSOX:
    def __init__(self, pin_scl, pin_sda, freq):
        self.device = I2C(1, scl = pin_scl, sda = pin_sda, freq = freq)
        self.int1 = Pin(13, Pin.IN)
        self.int2 = Pin(33, Pin.IN)
        self.fifo_over = 0
        self.data = []
    
    def scan(self):
        return self.device.scan()
    
# Write one byte     
    def write_8(self, addr, data):
        try:
            self.device.writeto_mem(LSM6DSOX_ADDR, addr, bytes([data]), addrsize = 8)
        except OSError:
            print('Failed to write the register' + str(addr))
# Read one byte  
    def read_8(self, addr):
        try :
            data = self.device.readfrom_mem(LSM6DSOX_ADDR, addr, 1)
        except OSError :
            print('Failed to read from register' + str(addr))
        return data[0]
    
# Read two bytes
    def read_16(self, addr):
        try :
            data = self.device.readfrom_mem(LSM6DSOX_ADDR, addr, 2)
        except OSError:
            print('Failed to read from register' + str(addr))
        return (data[1] << 8 | data[0])

# Configure the registers
    def load_settings(self):
        
        # Register watermark threshold for the depth of FIFO
        # FIFO buffer threshold is set to 54 * (1 byte tag + 6 bytes data)
        self.write_8(FIFO_CTRL1, 0x36)
        
        # Limit the FIFO depth to threshold - 8th bit is high
        self.write_8(FIFO_CTRL2, 0x80)
        
        # Register the batch data rate (26Hz) for the gyro and accelerometer
        self.write_8(FIFO_CTRL3, 0x22)
        
        # Register FIFO fill mode to continuous mode and time stamp decimation - odr/32
        self.write_8(FIFO_CTRL4, 0xA6)

        # Register output data rate (26Hz) and full scale (+/-16g) for accelerometer 
        self.write_8(CTRL1_XL, 0b00100100)
        
        # Register output data rate (26Hz) and full scale (+/-2000dps) for gyroscope
        self.write_8(CTRL2_G,  0b00101100)
        
        # Enable timestamp batching
#         self.write_8(CTRL10_C,  0b00100000)

        # Register wake up duration, free fall duration and its weight
        # """Not currently used for data collection"""
        self.write_8(WAKE_UP_DUR, 0b01000010)
        self.write_8(WAKE_UP_THS, 0b00000011)
        self.write_8(FREE_FALL, 0b0010011)
        self.write_8(TAP_CFG2, 0b10000000)

        # Register interrupt control register - fifo threshold interrupts to INT1, INT2 - no interrupts
        self.write_8(INT1_CTRL, int1_cfg)
        self.write_8(MD2_CFG, md2_cfg)
        self.write_8(MD1_CFG, md1_cfg)
        
# Check if the right sensor is connected, and load all settings/configuration registers                                                    
    def begin(self):
        if self.read_8(WHO_AM_I_REG) == 0x6c:
            self.load_settings()
            print('Device setup successful' )
        else:
            print('Failed to communicate with LSM6DSOX. Check connections')
        
# Poll interrupts                 
    def interrupt_en(self):
        self.fifo_over = 0
        if self.int1.value() or self.int2.value() :
            self.read_data()

# Read and store the FIFO data if an interrupt is detected                
    def read_data(self):
        i = 0
        self.data = []
        a = [0, 0, 0, 0]
        fifo_status = self.read_16(FIFO_STATUS1)
        fifo_full = fifo_status >> 15 
        fifo_size = int(fifo_status & 0x03FF)
        if fifo_full == 1:
            while (i <= fifo_size):
                a[0] = self.read_8(FIFO_DO_TAG) >>3
                a[1] = self.read_16(FIFO_DO_XL)
                a[2] = self.read_16(FIFO_DO_YL)
                a[3] = self.read_16(FIFO_DO_ZL)
                self.data = self.data + a
                i += 1
            self.fifo_over = 1
            
