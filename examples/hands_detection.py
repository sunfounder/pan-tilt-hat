from vilib import Vilib
from time import sleep

def main():
    Vilib.camera_start(vflip=True,hflip=True)
    Vilib.display(local=True,web=True)
    Vilib.hands_detect_switch(True)
    joints = []
    while True:
        joints = Vilib.detect_obj_parameter['hands_joints']
     
        if isinstance(joints,list) and len(joints) == 21:
            print(joints[8])

        sleep(1)


if __name__ == "__main__":
    main()