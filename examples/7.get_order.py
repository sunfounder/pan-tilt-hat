#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
# from ezblock import WiFi
# from ezblock import PWM
# from ezblock import Servo
# from ezblock import delay
from sunfunder_io import PWM,Servo
from time import sleep

Vilib.camera_start(True)
Vilib.traffic_sign_detect_switch(True)
# WiFi().write('CN', 'MakerStarsHall', 'sunfounder')

pwm_P1 = PWM("P1")

pwm_P0 = PWM("P0")


def forever():
    if (Vilib.traffic_sign_detect_object('type')) == 'stop':
        Servo(pwm_P1).angle(45)
        sleep(1)
    elif (Vilib.traffic_sign_detect_object('type')) == 'forward':
        Servo(pwm_P1).angle((-45))
        sleep(1)
    elif (Vilib.traffic_sign_detect_object('type')) == 'left':
        Servo(pwm_P0).angle(90)
        sleep(1)
    elif (Vilib.traffic_sign_detect_object('type')) == 'right':
        Servo(pwm_P0).angle((-90))
        sleep(1)
    Servo(pwm_P0).angle(0)
    Servo(pwm_P1).angle(0)
    
if __name__ == "__main__":
    while True:
        forever()  