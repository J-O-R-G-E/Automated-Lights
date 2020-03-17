#!/usr/bin/python3

"""
This program handles the relay for the lights.
"""

from time import sleep, localtime, strftime
from datetime import datetime
from astral import Astral # For sunset and sunrise
import RPi.GPIO as GPIO

def get_sun_status():
    # Gets time...
    now = strftime("%Y-%m-%d %H:%M:%S", localtime())
    year_list = now.split(' ')[0].split('-')
    time_list = now.split(' ')[1].split(':')

    # Gets sunset/sunrise
    city_name = 'Dallas' # For my region time
    a = Astral()
    a.solar_depression = 'civil' # Normal possition of the sun to the horizon.
    city = a[city_name]
    sun = city.sun(date=datetime.now(), local=True)
    sun_rise = int(str(sun['sunrise']).split(' ')[1].split(':')[0])
    sun_set = int(str(sun['sunset']).split(' ')[1].split(':')[0])
    
    return sun_rise, sun_set

def turn_switch_off(pinNum):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinNum,GPIO.OUT)
    GPIO.output(pinNum,1)
    
    return

def turn_switch_on(pinNum):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinNum,GPIO.OUT)
    GPIO.output(pinNum,0)

    return

def main():
    lights_are_on = False
    porch_lights_on = False
    
    while True:
        now = datetime.now()
        sun_rise, sun_set = get_sun_status()

        # Lets make our day start one hour before sunrise....
        if sun_rise-1 <= now.hour <= sun_set:
            if lights_are_on:
                # Turn porch lights off...
                turn_switch_off(23)
                porch_lights_on = False
                sleep(2)

                # Turn outside lights off...
                turn_switch_off(24)
                lights_are_on = False

                GPIO.cleanup()
                
            else:
                # Sleep for one hour every hour during the day...
                sleep(3601) 

        # At night...
        else:
            if not lights_are_on:                
                # Turn porch lichts on...
                turn_switch_on(23)
                porch_lights_on = True
                sleep(2)

                # Turn outside lights on...
                turn_switch_on(24)
                lights_are_on = True

            elif sun_set+3 == now.hour:
                # If we are here, we are three hours past sunset. Lets turn the porch lights off...
                if porch_lights_on:
                    turn_switch_off(23)
                    porch_lights_on = False
            else:
                sleep(3601) # sleep for an hour and a second 
                #continue            

    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram cancelled... \nCleaning up...\n")
        GPIO.cleanup()