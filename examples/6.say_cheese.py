#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
# from ezblock import WiFi
# from ezblock import print
# from ezblock import delay
from time import sleep

Vilib.camera_start(True)
Vilib.human_detect_switch(True)
# WiFi().write('CN', 'MakerStarsHall', 'sunfounder')


def forever():
    if (Vilib.human_detect_object('number')) >= 1:
        Vilib.get_picture(True)
        print("%s"%'OK')
        sleep(1000)

if __name__ == "__main__":
    while True:
        forever()  