from machine import Pin, I2C
from stemma_soil_sensor import StemmaSoilSensor # Save the two Libraries to the Pi Pico seesaw and stemma_soil_sensor
import time

SDA_PIN = 4 # GPIO 4 
SCL_PIN = 5 # GPIO 5

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

stemma_soil_sensor = StemmaSoilSensor(i2c)
seesaw = stemma_soil_sensor # Data Sheet = ~200 (very dry) to ~2000 (very wet) 1015 = Wet, 331 = Dry
                            # Soil sensor has temp + or - 2 degrees Celsius
pump = Pin(16, Pin.OUT) # Pump pin is connected to the transistor base, Pump is connected to 5v of PI Pico with a potentiometer in series to control flow.

def moisture_read():
  moisture = seesaw.get_moisture()
  temperature = seesaw.get_temp()
  print(f'Moisture Level: {moisture}, Temperature: {temperature:.1f}{chr(176)}C')
  time.sleep(2)
  if moisture < 415:
      if moisture >= 400 and moisture < 415:
          num_pump = 3
          print("REGULAR WATERING IN PROGRESS")
      elif moisture >= 370 and moisture < 400:
          num_pump = 5
          print("SLIGHTLY DRY: WATERING IN PROGRESS")
      elif moisture >= 340 and moisture < 270:
          print("DRY: WATERING IN PROGRESS")
          num_pump = 7
      else:
          print("VERY DRY: WATERING IN PROGRESS")
          num_pump = 9
    return num_pump

def pumping(num_pump):
  if num_pump > 0:
      for i in range(num_pump):
          pump.value(1) # turn pump on
          time.sleep(10) # pump will remain on for 10s
          
          pump.value(0) # turn pump off
          time.sleep(3) # pump will remain off for 10s
    print("<<Watering complete!>>\n")
    time.sleep(20) #1-2 minutes in final design 

while True:
    try:
        times_pump = moisture_read()
        if times_pump > 0:
          pumping(times_pump)
            
         
    except Exception as e:
        # Sensor reset after 10 sec
        print(f"Error,Resetting: {e}")
        time.sleep(10)
        i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
        stemma_soil_sensor = StemmaSoilSensor(i2c)
        seesaw = stemma_soil_sensor
        print("ERROR OCCURED:", e)
