import asyncio
from bleak import BleakClient, BleakScanner
import struct
import csv

# Auto generated UUIDs for service and characteristics (https://www.uuidgenerator.net/)
# These UUIDs must match what the ESP is advertising
ESP32_DEVICES = [
    {"name": "ESP32_BLE_1", "service_uuid": "5b6ad9a0-7e66-43c7-b4f8-b9d0c734393d", "char_uuid": "ee1247d7-6ac4-4bf6-b0b3-1828d127823c"},
    {"name": "ESP32_BLE_2", "service_uuid": "9cc5181a-3d5c-4e1b-b403-64972f680794", "char_uuid": "4e49e101-2044-458f-83e6-f35250d33740"}]

# Determines the file where the data is stored
OUTPUT_FILE_NAME = 'recieved_data.txt' 

# Handler for incoming data
async def recieve_data(device_name, sender, data):
    with open(device_name + '_' + OUTPUT_FILE_NAME, 'a', newline='') as f:
        values = struct.unpack('156h', data)
        writer = csv.writer(f)
        writer.writerows([values])


# Finds ESP32 in discoverable bluetooth devices
async def find_esp32(device):
    while True:

        # Gets a list of all devices and loops through them
        devices = await BleakScanner.discover()
        for d in devices:

            # If the name of the is in our device dictionary, return the device MAC Address
            if d.name == device["name"]:
                print(f"Found {device['name']}")
                return d.address  


        # Non-blocking sleep
        print(f"{device['name']} not found. Retrying in 2 seconds...")
        await asyncio.sleep(1)



# BLE handler for connection to ESP32 and data recieved
async def start_BLE(device):
    while True:
        
        # Gets the ESP32's address
        esp_address = await find_esp32(device)

        # Connects the client
        async with BleakClient(esp_address) as client:
            print(f"Connected to {device['name']}!")
            mtu = client.mtu_size
            print(f"MTU size: {mtu} bytes")

            # Starts a non-blocking callback for the notification handler
            # This will be called anytime data is transferred from the ESP32 to the PC
            await client.start_notify(device['char_uuid'], lambda s, d: asyncio.create_task(recieve_data(device['name'], s, d)))

            # If connected to the ESP32, non-blocking loop until disconnected
            while client.is_connected:
                await asyncio.sleep(1)

            # Prints that device has been disconnected
            print(f"{device['name']} disconnected. Reconnecting...")

        # Non-blocking sleep
        await asyncio.sleep(2)


# Gets ESP32 devices and runs BLE connection tasks for both
async def main():
    device_1, device_2 = ESP32_DEVICES
    await asyncio.gather(start_BLE(device_1), start_BLE(device_2))


# Runs the main function as async
if __name__ == "__main__":
    asyncio.run(main())
