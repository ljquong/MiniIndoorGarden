'''
# CHANGING VALUES FOR THE PUMP
def moisture_read():
    moisture = seesaw.get_moisture()
    temperature = seesaw.get_temp()
    print(f'Moisture Level: {moisture}, Temperature: {temperature:.1f}{chr(176)}C')
    time.sleep(2)
    num_pump = 0
    if moisture > 440:
        num_pump = 0
        print("WET: NO WATERING IN PROGRESS")
    elif moisture >= 440 and moisture < 400:
        num_pump = 2
        print("REGULAR WATERING IN PROGRESS")
    elif moisture <= 400: # or just else?
        print("DRY: WATERING IN PROGRESS")
        num_pump = 3        
    return num_pump

def pumping(num_pump):
    if num_pump > 0:
        for i in range(num_pump):
            pump.value(1) # turn pump on
            time.sleep(5) # pump will remain on for 5s
            pump.value(0) # turn pump off
            time.sleep(2) # pump will remain off for 2s
    print("<<Watering complete!>>\n")
    time.sleep(60) #1-2 minutes in final design
    '''
    
from machine import Pin, PWM, I2C
from stemma_soil_sensor import StemmaSoilSensor # Save the two Libraries to the Pi Pico seesaw and stemma_soil_sensor
import time

ldr = machine.ADC(28)
grow_lights = Pin(16, Pin.OUT)

# Initialize PWM pins for each color of the RGB LED
red = PWM(Pin(11, Pin.OUT))
green = PWM(Pin(12, Pin.OUT))
blue = PWM(Pin(13, Pin.OUT))

float_switch = Pin(10, Pin.IN, Pin.PULL_DOWN)

# Set all PWM pins to 1000 Hz frequency
red.freq(1000)
blue.freq(1000)
green.freq(1000)

SDA_PIN = 4 # GPIO 4 
SCL_PIN = 5 # GPIO 5

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

stemma_soil_sensor = StemmaSoilSensor(i2c)
seesaw = stemma_soil_sensor # Data Sheet = ~200 (very dry) to ~2000 (very wet) 1015 = Wet, 331 = Dry
                            # Soil sensor has temp + or - 2 degrees Celsius
pump = Pin(17, Pin.OUT) # Pump pin is connected to the transistor base, Pump is connected to 5v of PI Pico with a potentiometer in series to control flow.

# Function to set RGB LED color by converting 8-bit integers for
# r (red), g (green), b (blue) into 16-bit integers, that are
# used to set the duty cycles for the appropriate PWM pin
def set_color(r, g, b):
    red.duty_u16(r * 257)
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)

# set all lights to zero
set_color(0, 0, 0)
grow_lights.value(0)

# print statements are for testing only
# function to check ldr value to see if it is 'dark' for 10 seconds
# if it is, turn on the led lights, if it is 'not dark' for 10 seconds, turn lights off
# photocell must read 'dark' for ten seconds straight, otherwise final result will still be 'bright' and grow lights will not turn 
def read_photocell():
    is_dark = True
    for i in range(3):
        ldr_value = ldr.read_u16()
        if ldr_value < 60000:
            is_dark = False
        time.sleep(1)
    if is_dark:
        grow_lights.value(1)
        print(ldr_value)
        print("It is DARK.")
    else:
        grow_lights.value(0)
        print(ldr_value)
        print("It is BRIGHT.")

#read the state of the float switch: 0 means liquid present, so light should not turn on
#if there is no water, the light should turn on
def read_float_switch():
    if float_switch.value() == 0:
        set_color(0, 0, 0)
        print("There is WATER.")
    else:
        set_color(255, 0, 0)
        print("There is NO WATER.")

# CHANGING VALUES FOR THE PUMP
def moisture_read():
    moisture = seesaw.get_moisture()
    temperature = seesaw.get_temp()
    print(f'Moisture Level: {moisture}, Temperature: {temperature:.1f}{chr(176)}C')
    time.sleep(2)
    num_pump = 0
    if moisture > 440:
        num_pump = 0
        print("WET: NO WATERING IN PROGRESS")
    elif moisture <= 440 and moisture > 400:
        num_pump = 2
        print("REGULAR WATERING IN PROGRESS")
    elif moisture <= 400: # or just else?
        print("DRY: WATERING IN PROGRESS")
        num_pump = 3        
    return num_pump

def pumping(num_pump):
    for i in range(num_pump):
        pump.value(1) # turn pump on
        time.sleep(5) # pump will remain on for 5s
        pump.value(0) # turn pump off
        time.sleep(2) # pump will remain off for 2s
    print("<<Watering complete!>>\n")

# main program to run both functions continuously
while True:
    try:
        times_pump = 0
        pump.value(0)
        read_photocell()
        read_float_switch()
        times_pump = moisture_read()
        if times_pump > 0:
            pumping(times_pump)
            time.sleep(10) #1-2 minutes in final design
        time.sleep(2)            
    except Exception as e:
        # Sensor reset after 10 sec
        print(f"Error,Resetting: {e}")
        pump.value(0)
        time.sleep(10)
        i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        stemma_soil_sensor = StemmaSoilSensor(i2c)
        seesaw = stemma_soil_sensor
        pump.value (0)
        print("ERROR OCCURED:", e)

