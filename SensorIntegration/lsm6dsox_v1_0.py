from machine import I2C, Pin, Timer
from micropython import const

# SCL is Pin 20, SDA is Pin 22
a = []
read_timer = Timer(0)
i = 0
# Define register addresses

LSM6DSOX_I2C_ADDR 		= 	const(0x6A)
LSM6DSOX_FIFO_CTRL1 	= 	const(0x07)
LSM6DSOX_FIFO_CTRL2 	= 	const(0x08)
LSM6DSOX_FIFO_CTRL3 	= 	const(0x09)
LSM6DSOX_FIFO_CTRL4 	= 	const(0x0A)
LSM6DSOX_INT1_CTRL 		= 	const(0x0D)
LSM6DSOX_INT2_CTRL 		= 	const(0x0E)
LSM6DSOX_WHO_AM_I 		= 	const(0x0F)
LSM6DSOX_CTRL1_XL 		= 	const(0x10)
LSM6DSOX_CTRL2_G 		= 	const(0x11)
LSM6DSOX_WAKE_UP_SRC 	= 	const(0x1B)
LSM6DSOX_TAP_SRC		=	const(0x1C)
LSM6DSOX_FIFO_STATUS1	=	const(0x3A)
LSM6DSOX_FIFO_STATUS2	=	const(0x3B)
LSM6DSOX_WAKE_UP_THS	= 	const(0x5B)
LSM6DSOX_WAKE_UP_DUR	=	const(0x5C)
LSM6DSOX_FREE_FALL		=	const(0x5D)
LSM6DSOX_MD1_CFG		=	const(0x5E)
LSM6DSOX_MD2_CFG		=	const(0x5F)
LSM6DSOX_FIFO_DO_TAG	=	const(0x78)
LSM6DSOX_FIFO_DO_XL		=  	const(0x79)
LSM6DSOX_FIFO_DO_XH		=	const(0x7A)
LSM6DSOX_FIFO_DO_YL		=  	const(0x7B)
LSM6DSOX_FIFO_DO_YH		=	const(0x7C)
LSM6DSOX_FIFO_DO_ZL		=  	const(0x7D)
LSM6DSOX_FIFO_DO_ZH		=	const(0x7E)

# FIFO buffer threshold
buf_wtm 				=	const(0x1A)
bdr_gy			= 	const(0x1)
bdr_ac			=	const(0x2)
fifo_mode		=	const(0x6)
odr_ac			= 	const(0x2)
odr_gy			=	const(0x2)
fs_ac			=	const(0x2)
fs_gy			= 	const(0x1)
wu_lsb			=	const(0x1)
wu_dur			= 	const(0x04)
ff_th			=	const(0x3)
ff_dur			=	const(0x5)
int1_cfg		=	const(0b00101000)
int2_cfg		= 	const(0b10010000)




class Adafruit_LSM6DSOX:
    def __init__(self, pin_scl, pin_sda, freq):
        self.device = I2C(1, scl = pin_scl, sda = pin_sda, freq = freq)
    
    def _scan_(self):
        return self.device.scan()
    
    def _write_8(self, addr, data):
        self.device.writeto_mem(LSM6DSOX_I2C_ADDR, addr, bytes([data]), addrsize = 8)
    
    def _read_8(self, addr):
        data = self.device.readfrom_mem(LSM6DSOX_I2C_ADDR, addr, 1)
        return data[0]

    def _read_16(self, addr):
        data = self.device.readfrom_mem(LSM6DSOX_I2C_ADDR, addr, 2)
        return (data[1] << 8 | data[0])


    def _load_settings_(self):
        
# 		Register watermark threshold for the depth of FIFO
        self._write_8(LSM6DSOX_FIFO_CTRL1, (buf_wtm & 0xFF))
        self._write_8(LSM6DSOX_FIFO_CTRL2, (buf_wtm >> 8 & 0x01))
        
# 		Register the batch data rate for the gyro and accelerometer
        self._write_8(LSM6DSOX_FIFO_CTRL3, (bdr_ac << 4 | bdr_gy))
        
# 		Register FIFO fill mode
        self._write_8(LSM6DSOX_FIFO_CTRL4, (fifo_mode))

# 		Register output data rate and full scale value for accelerometer and gyroscope
        self._write_8(LSM6DSOX_CTRL1_XL, ((odr_ac << 4) | (fs_ac << 2)))
        self._write_8(LSM6DSOX_CTRL2_G,  ((odr_gy << 4) | (fs_gy << 2)))

# 		Register wake up duration, free fall duration and its weight
        self._write_8(LSM6DSOX_WAKE_UP_DUR, (wu_lsb << 4 & 0xff))
        self._write_8(LSM6DSOX_WAKE_UP_THS, (ff_dur & 0x80 | wu_dur))
        self._write_8(LSM6DSOX_FREE_FALL, (ff_dur << 3 | ff_th & 0x7))

# 		Register interrupt control register - fifo related interrupts to INT1, free fall/inactivity to INT2
        self._write_8(LSM6DSOX_INT1_CTRL, (int1_cfg))
        self._write_8(LSM6DSOX_MD2_CFG, (int2_cfg))
        

                                                    
    def begin(self):
        while self._read_8(LSM6DSOX_WHO_AM_I) != 0x6c:
            return False
        self._load_settings_()
        self.interrupt_en()
        return True
        
    def interrupt_en(self):
        int1.irq(trigger=Pin.IRQ_RISING, handler=read_data())
#         int2.irq(trigger=Pin. IRQ_RISING, handler=read_data)
        
        
def read_data():
    print (f'Reading data due to {int1.value()} and {int2.value()}')
    global i;
    i = 0
    y = p._read_16(LSM6DSOX_FIFO_STATUS1)
    x = int(y & 0x03FF)
    print(x)
    while (i <= x):
        a = p._read_8(LSM6DSOX_FIFO_DO_TAG)
        f = hex(a >> 3)
        b = p._read_16(LSM6DSOX_FIFO_DO_XL)
        c = p._read_16(LSM6DSOX_FIFO_DO_YL)
        d = p._read_16(LSM6DSOX_FIFO_DO_ZL)
        print((f), int(hex(b)), int(hex(c)), int(hex(d)))
        i += 1
    
        
        

p = Adafruit_LSM6DSOX(Pin(20), Pin(22), freq = 100000)
# Int1 at RX, Int2 at TX
int1 = Pin(7)
int2 = Pin(8)
print(p.begin())


    



    

                      

