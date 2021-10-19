#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
# from ezblock import WiFi
# from ezblock import print
# from ezblock import delay
# from ezblock import run_command

Vilib.camera_start()
Vilib.display()
Vilib.gesture_calibrate_switch(True)
# WiFi().write('CN', 'MakerStarsHall', 'sunfounder')
print("%s"%'Ready？Start the calibration!')
# delay(15000)
Vilib.gesture_calibrate_switch(False)

def forever():
    pass

if __name__ == "__main__":
    # try:
    while True:
        forever()  
    # finally:
        # run_command("sudo kill $(ps aux | grep '3.gesture_calibration.py' | awk '{ print $2 }')")
