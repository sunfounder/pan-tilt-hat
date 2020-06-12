#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
from ezblock import WiFi

Vilib.camera_start(True)
Vilib.traffic_sign_detect_switch(True)
WiFi().write('CN', 'MakerStarsHall', 'sunfounder')


def forever():
    pass

if __name__ == "__main__":
    while True:
        forever()  