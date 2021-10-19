#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib

Vilib.camera_start()
Vilib.display()
Vilib.traffic_sign_detect_switch(True)


def forever():
    pass

if __name__ == "__main__":
    while True:
        forever()  
