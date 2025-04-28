from machine import I2C, Pin, lightsleep
import time, esp32

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
TAP_CFG0		=	0x56
TAP_CFG2		=	0x58


start_fifo = 0
j = 0
ml_data = [[], [], [], []]


class Adafruit_LSM6DSOX:
    def __init__(self, pin_scl, pin_sda, freq):
        self.device = I2C(1, scl = pin_scl, sda = pin_sda, freq = freq)
        self.int1 = Pin(33, Pin.IN)
        self.int2 = Pin(32, Pin.IN)
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
    
# Configure FIFO settings
    def load_fifo_settings(self):
        # Register depth of FIFO threshold to 130d/0x82
        # 26 words (1 byte tag + 6 bytes data) per second
        # 2.5 seconds of both accelerometer and gyroscope data         
        self.write_8(FIFO_CTRL1, 0x82)
        
        # Limit the FIFO depth to threshold - 8th bit is high        
        self.write_8(FIFO_CTRL2, 0x80)

        # Register the batch data rate (26Hz) for the gyro and accelerometer
        self.write_8(FIFO_CTRL3, 0x22)
        
        # Register FIFO fill mode to continuous mode
        self.write_8(FIFO_CTRL4, 0x06)
        
        # Register interrupt control register - fifo threshold interrupts to INT1
        self.write_8(INT1_CTRL, 0x08)
        
#         self.fifo_interrupt_en()
    

# Configure the registers
    def load_settings(self):

        # Register output data rate (26Hz) and full scale (+/-16g) for accelerometer 
        self.write_8(CTRL1_XL, 0b00100100)
        
        # Register output data rate (26Hz) and full scale (+/-2000dps) for gyroscope
        self.write_8(CTRL2_G,  0b00101100)
        
        # Register wake up duration threshold set to 3 * (1/ODR) = 0.115s
        # Wake up lsb setting to FS_XL/2^6 = 0.25g
        # Sleep duration event to 1 * 512/ODR = 19.69s         
        self.write_8(WAKE_UP_DUR, 0b01100001)
        
        # Register wake-up threshold to 3 * 0.25g = 0.75g        
        self.write_8(WAKE_UP_THS, 0b00000011)
        
        # Enable the basic interrupts bit, activity/inactivity function (8th bit)
        # Sets accelerometer to low-power mode (12.5Hz)/ gyroscope in power-down
        # when in sleep mode (7-6th bits)         
        self.write_8(TAP_CFG2, 0b11100000)
        
        # Enable sleep status reporting on INT2 pins
        self.write_8(TAP_CFG0, 0x20)

        # Register interrupt control register to detect inactivity/activity on INT2
        self.write_8(MD2_CFG, 0x80)
           
        
# Check if the right sensor is connected, and load all settings/configuration registers                                                    
    def begin(self):
        if self.read_8(WHO_AM_I_REG) == 0x6c:
            self.load_settings()
            print('Device setup successful' )
        else:
            print('Failed to communicate with LSM6DSOX. Check connections')
        
# Poll fifo interrupts                 
    def fifo_interrupt_en(self):
        self.fifo_over = 0
        if self.int1.value():
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
        
    def collect_data(self):
        global j
        self.fifo_interrupt_en()
        if self.fifo_over == 1:
            ml_data[j] = self.data
            print(ml_data[j])
            print(f"New data of ID {j} collected at {time.ticks_ms()}")
            j = (j + 1) % 4


def initialize_IMU():
    global p
    p = Adafruit_LSM6DSOX(Pin(20), Pin(22), freq=100000)
    p.begin()
    esp32.wake_on_ext0(pin=p.int2, level=esp32.WAKEUP_ALL_LOW)
    while True:
        if p.int2.value() == 0 :
            p.load_fifo_settings()
            p.collect_data()
        else:
            print(f"Going to sleep at {time.ticks_ms()}")
            print(f"Sleep")
            lightsleep()


initialize_IMU()


   

    
            
