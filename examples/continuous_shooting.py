#!/usr/bin/env python3
from time import sleep,strftime,localtime
from vilib import Vilib
import sys
sys.path.append('./')
from servo import Servo
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



manual = '''
Press keys on keyboard to record value!
    W: up
    A: left
    S: down
    D: right
    Q: continuous_shooting

    G: Quit
'''

# region servos init
pan = Servo(pin=13, min_angle=-90, max_angle=90) # pan_servo_pin (BCM)
tilt = Servo(pin=12, min_angle=-90, max_angle=30) # be careful to limit the angle of the steering gear
panAngle = 0
tiltAngle = 0
pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)
#endregion init

# region servo control
def limit(x,min,max):
    if x > max:
        return max
    elif x < min:
        return min
    else:
        return x

def servo_control(key):
    global panAngle,tiltAngle       
    if key == 'w':
        tiltAngle -= 1
        tiltAngle = limit(tiltAngle, -90, 30)
        tilt.set_angle(tiltAngle)
    if key == 's':
        tiltAngle += 1
        tiltAngle = limit(tiltAngle, -90, 30)
        tilt.set_angle(tiltAngle)
    if key == 'a':
        panAngle += 1
        panAngle = limit(panAngle, -90, 90)
        pan.set_angle(panAngle)
    if key == 'd':
        panAngle -= 1
        panAngle = limit(panAngle, -90, 90)
        pan.set_angle(panAngle)

# endregion

# continuous shooting 
def continuous_shooting(path,interval_ms:int=50,number=10):
    print("continuous_shooting .. ")
    path=path+'/'+strftime("%Y-%m-%d-%H.%M.%S", localtime())
    for i in range(number):
        Vilib.take_photo(photo_name='%03d'%i,path=path)
        print("take_photo: %s"%i)
        sleep(interval_ms/1000)
    print("continuous_shooting done,the pictures save as %s"%path)
    sleep(0.2)

def main():

    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)

    path = "/home/pi/Pictures/vilib/continuous_shooting"
  
    print(manual)
    while True:
        key = readchar().lower()
        servo_control(key)
        if key == 'q': 
            continuous_shooting(path,interval_ms=50,number=10)
        elif key == 'g':
            Vilib.camera_close()
            break 
        sleep(0.01)


if __name__ == "__main__":
    main()

    