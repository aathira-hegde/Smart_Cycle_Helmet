from machine import I2C, Pin, deepsleep
import machine
import time, esp32
from time import sleep
import RandomForest
from bluetooth import BLE
import ubluetooth

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
        self.int1 = Pin(32, Pin.IN)
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
    
# Configure FIFO settings
    def load_fifo_settings(self):
        # Register depth of FIFO threshold to 130d/0x82
        # 26 words (1 byte tag + 6 bytes data) per second
        # 2.5 seconds of both accelerometer and gyroscope data         
        self.write_8(FIFO_CTRL1, 0x34)
        
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
            #print(ml_data[j])
            #print(f"New data of ID {j} collected at {time.ticks_ms()}")
            j = (j + 1) % 4
            IMU_Data = [self.to_signed_int16(x) for x in p.data]
            features_Dictonary = RandomForest.calculate_kinematic_features(IMU_Data)
            features = [features_Dictonary[key] for key in features_Dictonary]
            prediction = RandomForest.predictLabel(features)
            print(prediction)
            global ble_peripheral
            ble_peripheral.send_data(prediction)
            if(prediction=='Braking'):
                global RearLight_timer
                RearLight.value(1)
                RearLight_timer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=Turn_RearLight_OFF)
    def to_signed_int16(self,value):
        return value - 65536 if value >= 32768 else value
class BLEPeripheral:
    def __init__(self):
        self.name = 'Smart Cycle Helmet'
        
        # create a BLE object and set it to Active
        self.ble = BLE()
        self.ble.active(True)
        
        # Sets MTU to 512 Bytes of data to transfer
        self.ble.config(mtu=512) # 256 if this b
        self.mtu = 512
        print('MTU: ', self.ble.config('mtu'))
        
        # Creates a call back function for BLE when an event happens
        self.ble.irq(self.ble_irq)

        # Example modified from https://docs.micropython.org/en/latest/library/bluetooth.html#bluetooth.BLE.gatts_register_services Heart Rate Service
        # Auto generated UUIDs for service and characteristics (https://www.uuidgenerator.net/)
        self.imu_uuid = ubluetooth.UUID("5b6ad9a0-7e66-43c7-b4f8-b9d0c734393d")
        self.char_uuid = ubluetooth.UUID("ee1247d7-6ac4-4bf6-b0b3-1828d127823c")

        # Define characteristic with notify permission
        self.imu_char = (self.char_uuid, ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY)
        self.imu_service = (self.imu_uuid, (self.imu_char,))

        # Register service and store characteristic handle, extracts the actual int from the returned tuple
        ((self.imu_handle,),) = self.ble.gatts_register_services([self.imu_service])
        
        # Boolean to track whether we are conencted or not
        self.connected = False
        
        # Calls advertise function to become discoverable
        self.advertise()
        
        return 
    # Advertise ble
    def advertise(self):
        
        # Indicates the device will be BLE only and in general discovarable mode
        adv_data = bytearray(b'\x02\x01\x06')
        
        # Encodes the device name for the advertising data
        adv_data = adv_data + bytearray((len(self.name) + 1, 0x09))
        adv_data = adv_data + self.name.encode()

        # Advertises the device with a 100ms interval
        self.ble.gap_advertise(100, adv_data)

    def ble_irq(self, event, data):
        # If connect to a device, set connected to True
        if event == 1:
            self.connected = True
            print("Connected")
            
        # If disconnect from the device, set connected to false, re-advertize
        elif event == 2:
            self.connected = False
            print("Disconnected")
            self.advertise()

    # Sends data to a connected device
    def send_data(self,CurrentPrediction):

        if self.connected:
            # Write the local value for the handle and sends an update to the client
            self.ble.gatts_write(self.imu_handle, CurrentPrediction, True)

def Turn_RearLight_OFF(_timer):
    global RearLight
    RearLight.value(0)
def initialize_IMU():
    global p
    global ble_peripheral
    ble_peripheral = BLEPeripheral()
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
            deepsleep()

NEOI2C_PWR = Pin(2, Pin.OUT)
NEOI2C_PWR.value(0)
sleep(0.5)
NEOI2C_PWR.value(1)
RearLight = Pin(13, Pin.OUT)		
RearLight.value(0)
RearLight_timer = machine.Timer(1) 	#Use HW timer 1 to turn on rear light for 3 seconds

initialize_IMU()


   

    
            
