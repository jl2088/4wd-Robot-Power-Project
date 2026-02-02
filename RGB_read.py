from ws2812 import WS2812
from machine import I2C, Pin
import time
import struct

LIGHT_PIN = 19
LIGHT_NUM = 24

LIGHT_REAR_RIGHT = [0, 1]
LIGHT_REAR_MIDDLE = [2, 3, 4, 5]
LIGHT_REAR_LEFT = [6, 7]
LIGHT_REAR = [0, 1, 2, 3, 4, 5, 6, 7]
light_rear = [LIGHT_REAR_RIGHT, LIGHT_REAR_MIDDLE, LIGHT_REAR_LEFT] # Two-dimensional array

LIGHT_BOTTOM_LEFT = [8, 9, 10, 11, 12, 13, 14, 15]
LIGHT_BOTTOM_RIGHT = [16, 17, 18, 19, 20, 21, 22, 23]
light_bottom = [LIGHT_BOTTOM_LEFT, LIGHT_BOTTOM_RIGHT] # Two-dimensional array

all_light = [LIGHT_REAR, LIGHT_BOTTOM_LEFT, LIGHT_BOTTOM_RIGHT] # Two-dimensional array

np = WS2812(LIGHT_PIN, LIGHT_NUM)

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

def get_address(i2c):
    devices = i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found.")
        return 0x40 # Default address of I2C
    else:
        for device in devices:
            return device

def set_off():
    set_all_color([0, 0, 0])

# INA3221's I2C address is usually 0x40
ina3221_address = get_address(i2c)
channel_1_current_addr = 0x01 # Channel 1 current register address
channel_2_voltage_addr = 0x03 # Channel 2 Voltage register address

def set_all_color(color): # O(n)
    ''' set color to all lights 
        color list or hex, 1*3 list, the order is [red, green, blue] 
    '''
    for i in range(24):
        np[i] = color
    np.write()
    
def set_all_color_complex(color): # O(n^2)
    for light in all_light:
        for i in light:
            np[i] = color
        np.write()


def set_bottom_color(color): # O(n)
    for num in LIGHT_BOTTOM_LEFT:
        np[num] = color
    for num in LIGHT_BOTTOM_RIGHT:
        np[num] = color
    np.write()
    
def set_bottom_color_complex(color): # O(n^2)
    for light in light_bottom:
        for num in light:
            np[num] = color
        np.write() # As same as function set_bottom_color

def set_rear_color(color): # O(n)
    for num in LIGHT_REAR:
        np[num] = color
    np.write()
    
def set_rear_color_complex(color): # O(n^2)
    for light in light_rear:
        for num in light:
            np[num] = color
        np.write() # As same as function set_rear_color

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

def write_file(file,rate):
    t = 1000/rate # ms
    for i in range(rate): # Running in one second
        current = read_ina3221_current()
        voltage = read_ina3221_voltage()
        file.write(f"Channel 1 - Current: {current} A\n")
        file.write(f"Channel 2 - Voltage: {voltage} V\n")
        time.sleep_ms(int(t)-3) # Reading and writing will cost about 3ms

# call function
if __name__ == "__main__":
    rate = 10 # or 2, 5 (times per sec)
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255]]
    with open('./log.txt', 'w') as file:
        try:
            for i in colors:
#*****************Original Code*****************
                set_all_color(i)
#*****Original Code (higher time complexity)****
                set_all_color_complex(i)
#****************Double Function****************
                set_bottom_color(i)
                set_rear_color(i)
#****Double Function (higher time complexity)****
                set_bottom_color_complex(i)
                set_rear_color_complex(i)
# Annotate other methods to test a single method
                write_file(file, rate)
        finally:
            set_off()