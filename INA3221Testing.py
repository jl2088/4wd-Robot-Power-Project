from machine import I2C, Pin
import time
import struct

# Initialize the I2C bus and select the GPIO pins connected to the INA3221
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Check I2C
def get_address(i2c):
    devices = i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found.")
    else:
        for device in devices:
            return device

# INA3221's I2C address is usually 0x40
ina3221_address = get_address(i2c) # Or 0x43

# INA3221 Register Addresses
# Register addresses for Channel 1 current measurement and Channel 2 voltage measurement
channel_1_current_addr = 0x01 # Channel 1 current register address
channel_2_voltage_addr = 0x03 # Channel 2 Voltage register address


def read_ina3221_current():
    # Read current data from channel 1 of INA3221, with 2 bytes per channel
    data = i2c.readfrom_mem(ina3221_address, channel_1_current_addr, 2)
    # Analyze as current value
    current_raw = struct.unpack('>h', data)[0]
    current = current_raw / 20000.0  # Convert the original value to the actual current value
    return round(current, 3)  # Keep three decimal places

def read_ina3221_voltage():
    # Read voltage data from channel 2 of INA3221, with 2 bytes per channel
    data = i2c.readfrom_mem(ina3221_address, channel_2_voltage_addr, 2)
    # Analyze as current value
    voltage_raw = struct.unpack('>h', data)[0]
    voltage = voltage_raw / 8.7  # Convert the original value to the actual current value
    return round(voltage, 3)  # Keep three decimal places

# Main loop
with open('./log.txt', 'w') as file: # Open recording file (log.txt)
    try:
        while True:
            # Read current and voltage data from channels of INA3221
            current = read_ina3221_current()
            voltage = read_ina3221_voltage()

            # Record and display current and voltage information
            file.write(f"Channel 1 - Current: {current} A\n")
            file.write(f"Channel 2 - Voltage: {voltage} V\n")
            print(f"Channel 1 - Current: {current} A")
            print(f"Channel 2 - Voltage: {voltage} V")

            # Wait for a period of time to control the update frequency
            time.sleep(1)

    except KeyboardInterrupt:
        # Capture keyboard interrupts to exit the loop
        pass