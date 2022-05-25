#!/usr/bin/env python3
from vilib import Vilib
import time

color_flag = 'close'
color_list = ['close', 'red','orange','yellow','green','blue','purple']

manual = '''
Input key to call the function!
    1: Color detect : red
    2: Color detect : orange
    3: Color detect : yellow
    4: Color detect : green
    5: Color detect : blue
    6: Color detect : purple
    0: Switch off Color detect

    S: Display detected object information
    Q: Photo shoot
    G: Quit
'''

def color_detect(color):
    if color == 'close':
        print("Color detect off!")
        Vilib.color_detect_switch(False)
    else:
        print("detecting color :" + color)
        Vilib.color_detect(color)


def show_info():
    if color_flag == 'close':
        print("Color detection is turned off !")
    else:
        if Vilib.detect_obj_parameter['color_n']!=0:
            color_coodinate = (Vilib.detect_obj_parameter['color_x'],Vilib.detect_obj_parameter['color_y'])
            color_size = (Vilib.detect_obj_parameter['color_w'],Vilib.detect_obj_parameter['color_h'])
            print("Coordinate:",color_coodinate,"Size",color_size)
        else:
            print("No %s detected!"%color_flag)


def main():
    global color_flag
    path = "/home/pi/Pictures/vilib/color_detection/"

    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)
    time.sleep(2)
    
    print(manual)
    while True:
        try:
            key = input().lower()
            if key in ['0', '1', '2', '3', '4', '5', '6']:
                color_flag = color_list[int(key)]
                color_detect(color_flag)
            elif key == "s":
                show_info()
            elif key == 'q':
                _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
                Vilib.take_photo(photo_name=str(_time),path=path)
                print("The photo save as %s%s.jpg"%(path,_time))
            elif key == "g" :
                Vilib.camera_close()
                break 
        except KeyboardInterrupt:
            Vilib.camera_close()
            break


if __name__ == "__main__":
    main()

