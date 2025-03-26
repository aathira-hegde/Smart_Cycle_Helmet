from machine import Pin, I2C
import time
import math

# I2C Initialization - USE THE CORRECT ADDRESS!
i2c = I2C(1, scl=Pin(20), sda=Pin(22))  # Example: ESP32 pins
lsm6dsox_address = 0x6A  # CHANGE THIS if necessary

# LSM6DSOX Register Addresses
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
FIFO_CTRL1 = 0x06
FIFO_CTRL2 = 0x07
FIFO_CTRL5 = 0x0A
FIFO_STATUS2 = 0x3B
OUTX_L_G = 0x22
OUTX_L_XL = 0x28

# Global variables
gyro_bias_x = 0.0
gyro_bias_y = 0.0
gyro_bias_z = 0.0

# --- Helper Functions ---

def read_register(address, register):
    """Reads a byte from a register."""
    i2c.writeto(address, bytes([register]))
    return i2c.readfrom(address, 1)[0]

def read_registers(address, register, num_bytes):
    """Reads multiple bytes from a register."""
    i2c.writeto(address, bytes([register]))
    return i2c.readfrom(address, num_bytes)

def write_register(address, register, value):
    """Writes a byte to a register."""
    i2c.writeto_mem(address, register, bytes([value]))

def standard_deviation(data):  # Keep this for calibration
    """Calculates the standard deviation of a list of numbers."""
    n = len(data)
    if n < 2:
        return 0.0
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    return variance ** 0.5

# --- Sensor Functions ---

def get_accel_data():
    """Reads and scales accelerometer data."""
    try:
        data = read_registers(lsm6dsox_address, OUTX_L_XL, 6)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        x = x if x < 32768 else x - 65536
        y = y if y < 32768 else y - 65536
        z = z if z < 32768 else z - 65536
        scale = 0.061 / 1000  # mg/LSB at 2g range to g's
        return x * scale, y * scale, z * scale
    except Exception as e:
        print("Error reading accelerometer data:", e)
        return 0.0, 0.0, 0.0

def get_gyro_data():
    """Reads and scales gyroscope data (from FIFO)."""
    global gyro_bias_x, gyro_bias_y, gyro_bias_z

    try:
        data = read_registers(lsm6dsox_address, OUTX_L_G, 6)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        x = x if x < 32768 else x - 65536
        y = y if y < 32768 else y - 65536
        z = z if z < 32768 else z - 65536
        scale = 8.75 / 1000  # mdps/LSB at 250 dps range to dps

        x *= scale
        y *= scale
        z *= scale

        # --- Dynamic Offset Adjustment (Only When Still) ---
        stillness_threshold = 1.0  #  Reduced threshold
        dynamic_calibration_rate = 0.0001 # Reduced rate

        if abs(x) < stillness_threshold and abs(y) < stillness_threshold and abs(z) < stillness_threshold:
            gyro_bias_x += (x - gyro_bias_x) * dynamic_calibration_rate
            gyro_bias_y += (y - gyro_bias_y) * dynamic_calibration_rate
            gyro_bias_z += (z - gyro_bias_z) * dynamic_calibration_rate
        return x - gyro_bias_x, y - gyro_bias_y, z - gyro_bias_z

    except Exception as e:
        print("Error reading gyroscope data:", e)
        return 0.0, 0.0, 0.0
# --- Calibration ---
def calibrate_gyro(num_samples=500, stable_threshold=0.5, max_retries=5):
    """Improved gyroscope calibration with stability check and retry mechanism."""
    global gyro_bias_x, gyro_bias_y, gyro_bias_z
    print("Calibrating gyroscope.  Keep the sensor VERY still...")
    retries = 0

    while retries < max_retries:
        sums = [0.0, 0.0, 0.0]  # Reset sums on each retry
        values = [[], [], []]  # Reset values on each retry
        for i in range(num_samples):
            # Get raw gyro data
            try:
                data = read_registers(lsm6dsox_address, OUTX_L_G, 6)
                x = (data[1] << 8) | data[0]
                y = (data[3] << 8) | data[2]
                z = (data[5] << 8) | data[4]
                x = x if x < 32768 else x - 65536
                y = y if y < 32768 else y - 65536
                z = z if z < 32768 else z - 65536
                scale = 8.75 / 1000
                x *= scale
                y *= scale
                z *= scale

            except Exception as e:
                print("Error during calibration read:", e)
                # Instead of restarting immediately, count this as a retry
                retries += 1
                time.sleep(0.1) # Short delay
                break  # Exit the inner loop and retry

            sums[0] += x
            sums[1] += y
            sums[2] += z
            values[0].append(x)
            values[1].append(y)
            values[2].append(z)

            time.sleep(0.01)

            if i > 100 and i % 50 == 0:
                std_dev_x = standard_deviation(values[0])
                std_dev_y = standard_deviation(values[1])
                std_dev_z = standard_deviation(values[2])

                if (std_dev_x > stable_threshold or
                    std_dev_y > stable_threshold or
                    std_dev_z > stable_threshold):
                    print(f"Sensor not stable (attempt {retries + 1}/{max_retries}). Retrying...")
                    retries += 1
                    time.sleep(0.5)  # Wait a bit before retrying
                    break  # Exit the inner loop and retry
        else:  # This 'else' belongs to the 'for' loop
            # Calibration successful (inner loop completed without breaking)
            gyro_bias_x = sums[0] / num_samples
            gyro_bias_y = sums[1] / num_samples
            gyro_bias_z = sums[2] / num_samples
            print("Calibration complete.")
            print(f"Gyro biases: x={gyro_bias_x:.4f}, y={gyro_bias_y:.4f}, z={gyro_bias_z:.4f}")

            return True  # Calibration succeeded!

    print("Calibration failed after multiple retries. Check sensor and environment.")
    # Reset biases if calibration ultimately fails
    gyro_bias_x = 0.0
    gyro_bias_y = 0.0
    gyro_bias_z = 0.0
    return False # Indicate that the calibration failed
# --- Initialization ---

def init_sensor():
    """Initializes the sensor, including FIFO configuration."""
    try:
        # Set accelerometer to 416 Hz, 2g range
        write_register(lsm6dsox_address, CTRL1_XL, 0x80)  # 416 Hz

        # Set gyroscope to 416 Hz, 250 dps range
        write_register(lsm6dsox_address, CTRL2_G, 0x80)  # 416 Hz

        # Enable Block Data Update (BDU) -- IMPORTANT!
        write_register(lsm6dsox_address, CTRL3_C, 0x44)  # BDU enabled, auto-increment

        # --- FIFO Configuration ---

        # FIFO Mode: Continuous (overwrites oldest data when full)
        # Set FIFO ODR to 104 Hz (a decimation factor of 4 from 416 Hz)
        # Store *only* gyroscope data in the FIFO.
        write_register(lsm6dsox_address, FIFO_CTRL5, 0b01101000) # 0b011(ODR 104Hz)010(Gyro Only)00
		# FIFO threshold - set to 1 (read as soon as data is available)
        write_register(lsm6dsox_address, FIFO_CTRL1, 1)
        write_register(lsm6dsox_address, FIFO_CTRL2, 0x00)

        return True

    except Exception as e:
        print("Error initializing sensors:", e)
        return False

# --- Main Program ---

if init_sensor():
    if calibrate_gyro():
        target_period_us = 100000  # Target period: 0.1 seconds (100,000 microseconds)
        last_read_time = time.ticks_us()

        while True:
            try:
                accel_x, accel_y, accel_z = get_accel_data()
                gyro_x, gyro_y, gyro_z = get_gyro_data()


                # --- FIFO Status Check (Important!) ---
                fifo_status = read_register(lsm6dsox_address, FIFO_STATUS2)
                if (fifo_status & 0x80):  # Check for FIFO overrun (bit 7)
                    print("FIFO OVERRUN! Data lost.")

                # --- Precise Timing ---
                current_time = time.ticks_us()
                elapsed_time = time.ticks_diff(current_time, last_read_time)
                
                # Only print if it has been at least target_period_us
                if elapsed_time >= target_period_us:
                    print("Accel: {:.4f} {:.4f} {:.4f}  Gyro: {:.4f} {:.4f} {:.4f}".format(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z))
                    last_read_time = current_time #Update the last time we printed

                #Always sleep a little bit to avoid locking up the system.
                time.sleep_us(100)

            except Exception as e:
                print("Error in main loop:", e)
                time.sleep(1)
    else:
        print("Calibration failed.  Program will not run.")
else:
    print("Sensor initialization failed.")
