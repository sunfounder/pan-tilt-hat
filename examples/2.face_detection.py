#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
# from ezblock import WiFi
# from ezblock import print

Vilib.camera_start()
Vilib.display()
Vilib.human_detect_switch(True)
# WiFi().write('CN', 'MakerStarsHall', 'sunfounder')


def forever():
    print("%s"%(''.join([str(x) for x in ['There are ', Vilib.human_detect_object('number'), ' people']])))

if __name__ == "__main__":
    while True:
        forever()  