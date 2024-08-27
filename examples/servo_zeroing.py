#!/usr/bin/env python3
import sys
sys.path.append('./')
from servo import Servo
from time import sleep

pan = Servo(pin=13) # pan_servo_pin (BCM)
tilt = Servo(pin=12) 

pan.set_angle(10)
tilt.set_angle(10)
sleep(0.2)
pan.set_angle(0)
tilt.set_angle(0)
while True:
    pass

