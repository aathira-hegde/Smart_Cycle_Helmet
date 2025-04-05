from machine import Timer, Pin
from bluetooth import BLE
import ubluetooth
import struct
from time import sleep
import machine

from i2c_peripheral import Adafruit_LSM6DSOX
i = 0
NEOI2C_PWR = Pin(2, Pin.OUT)
NEOI2C_PWR.value(0)
sleep(0.5)
NEOI2C_PWR.value(1)
p = Adafruit_LSM6DSOX(Pin(20), Pin(22), freq = 100000)
p.begin()

class BLEPeripheral:
    StartSendingData = 0
    def __init__(self):
        self.name = 'ESP32_BLE_1'
        
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
        
        #self.loop()

        # Counter to test data being sent
#         self.counter = 0
#         self.timer = Timer(0)
#         self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.send_data)
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
    def send_data(self):
        if self.connected:
                
            # Sending IMU data              
            simulate_payload = p.data
            
            # Converts data to hex
            # Pack as 2 byte signed integers
            # 120h = 120 2-byte signed short, 156h = 156 2-byte signed short
            # MAX THIS CAN BE is 
            data = struct.pack('156h', *simulate_payload)

            
            # Write the local value for the handle and sends an update to the client
            self.ble.gatts_write(self.imu_handle, data, True)
            print(f"Sent data")
        else:
            print("No device connected")

    # Continuously polls for FIFO interrupts and sends data if detected      
    def loop(self):
        print("Start loop")
        while(1):
            p.interrupt_en()
            if p.fifo_over == 1:
                print('Fifo status detected')
                if(self.StartSendingData>0):
                    self.send_data()
                    self.StartSendingData -= 1
                    print("Sending IMU batch",10-self.StartSendingData)
            else:
                pass
def switch_callback(pin):
    global ble_peripheral
    ble_peripheral.StartSendingData = 10
    print("Start recording IMU data")
    sleep(0.2)

m_switch = Pin(38, Pin.IN)				#Initialize Switch38 on ESP32 Feather V2 board            
m_switch.irq(trigger=machine.Pin.IRQ_FALLING, handler=switch_callback)

        
ble_peripheral = BLEPeripheral()
ble_peripheral.loop()

