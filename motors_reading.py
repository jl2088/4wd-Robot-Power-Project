from machine import Pin, PWM, I2C
import time
import struct

def mapping(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Motor(): # This part of the code was from Pico's examples
    def __init__(self, pin_a, pin_b, dir=1):
        self.pwm1 = PWM(Pin(pin_a, Pin.OUT))
        self.pwm2 = PWM(Pin(pin_b, Pin.OUT))
        self.pwm1.freq(20000)
        self.pwm2.freq(20000)
        self.dir = dir
        self.current_power = 0

    def run(self, power:int):
        self.current_power = power
        if power == 0:
            self.pwm1.duty_u16(0xffff)
            self.pwm2.duty_u16(0xffff)
        else:
            value = mapping(abs(power), 0, 100, 20, 100)
            value = int(value / 100.0 * 0xffff)

            if power*self.dir > 0:
                self.pwm1.duty_u16(0xffff - value)
                self.pwm2.duty_u16(0xffff)
            else:
                self.pwm1.duty_u16(0xffff)
                self.pwm2.duty_u16(0xffff - value)

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

def get_address(i2c):
    devices = i2c.scan()
    if len(devices) == 0:
        print("No I2C devices found.")
        return 0x40 # Default address of I2C
    else:
        for device in devices:
            return device

# INA3221's I2C address is usually 0x40
ina3221_address = get_address(i2c)
channel_1_current_addr = 0x01 # 0x01  # Channel 1 current register address (example, needs to be adjusted according to actual situation)
channel_2_voltage_addr = 0x03 #0x03  # Channel 2 Voltage register address (example, needs to be adjusted according to actual situation)

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

if __name__ == '__main__':

    # initialize motors
    left_front  = Motor(17, 16, dir=-1)
    right_front = Motor(15, 14, dir= 1)
    left_rear   = Motor(13, 12, dir=-1)
    right_rear  = Motor(11, 10, dir= 1)

    with open('./log.txt', 'w') as file:
        try:
            # forward
            power = 80
            rate = 2 # or 5
            left_front.run(power)
            right_front.run(power)
            left_rear.run(power)
            right_rear.run(power)
            for i in range(30): # 30 seconds or 12 seconds
                write_file(file, rate)

        finally:
            # stop
            power = 0
            left_front.run(power)
            right_front.run(power)
            left_rear.run(power)
            right_rear.run(power)  
