#!/usr/bin/env python3
from vilib import Vilib
import time

manual = '''
Press keys on keyboard to record value!
    Q: photo shoot
    G: Quit
'''

def main():
    path = "/home/pi/Pictures/vilib/"

    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)
    time.sleep(2)

    print(manual)
    while True:
        try:
            key = input().lower()
            if key == "q":
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

    