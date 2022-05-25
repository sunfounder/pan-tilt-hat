#!/usr/bin/env python3
from vilib import Vilib
from time import sleep


def object_show():
    print("Number: ",Vilib.detect_obj_parameter['human_n'])
    human_coodinate = (Vilib.detect_obj_parameter['human_x'],Vilib.detect_obj_parameter['human_y'])
    human_size = (Vilib.detect_obj_parameter['human_w'],Vilib.detect_obj_parameter['human_h'])
    print("Coordinate:",human_coodinate,"Size",human_size)

def main():
    Vilib.camera_start(vflip=True,hflip=True)
    Vilib.display(local=True,web=True)
    Vilib.human_detect_switch(True)  

    while True:
        object_show()
        sleep(0.2)
            

if __name__ == "__main__":
    main()

    