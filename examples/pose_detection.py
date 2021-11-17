from time import sleep
from vilib import Vilib


def main():
    
    Vilib.camera_start(vflip=True,hflip=True)
    Vilib.display(local=True,web=True)
    Vilib.pose_detect_switch(True)

    joints = []
    while True:
        joints = Vilib.detect_obj_parameter['body_joints']
        
        if isinstance(joints,list) and len(joints) == 33:
            print(joints[15])

        sleep(1)

if __name__ == "__main__":
    main()
