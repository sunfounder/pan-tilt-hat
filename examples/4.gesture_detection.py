#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
from ezblock import WiFi
from ezblock import delay
from ezblock import print
ges1 = None
ges2 = None
ges3 = None

Vilib.camera_start(True)
Vilib.gesture_detect_switch(True)
WiFi().write('CN', 'MakerStarsHall', 'sunfounder')


def forever():
    global ges1, ges2, ges3
    ges1 = Vilib.gesture_detect_object('type')
    delay(50)
    ges2 = Vilib.gesture_detect_object('type')
    delay(50)
    ges3 = Vilib.gesture_detect_object('type')
    if ges1 == ges2 and ges1 == ges3:
        print("%s"%ges1)

if __name__ == "__main__":
    while True:
        forever()  