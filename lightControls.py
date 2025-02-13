from machine import Pin, PWM
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

# Function to set RGB LED color by converting 8-bit integers for
# r (red), g (green), b (blue) into 16-bit integers, that are
# used to set the duty cycles for the appropriate PWM pin
def set_color(r, g, b):
    red.duty_u16(r * 257)
    green.duty_u16(g * 257)
    blue.duty_u16(b * 257)

# Turn all lights off
set_color(0, 0, 0)
grow_lights.value(0)

# function to check ldr value to see if it is 'dark' for 10 seconds
# if it is, turn on the led lights, if it is 'not dark' for 10 seconds, turn lights off
def read_photocell():
    is_dark = True
    for i in range(10):
        ldr_value = ldr.read_u16()
        if ldr_value < 60000:
            is_dark = False
        time.sleep(1)
    if is_dark:
        grow_lights.value(1)
    else:
        grow_lights.value(0)

# read the state of the float switch: 0 means liquid present, so light should not turn on
# if there is no water, the light should turn on
def read_float_switch():
    if float_switch.value() == 0:
        set_color(0, 0, 0)
    else:
        set_color(255, 0, 0)

# main program to run both functions continuously
while True:
    read_photocell()
    read_float_switch()
    time.sleep(1)
