from time import perf_counter, sleep,strftime,localtime
from vilib import Vilib
from sunfounder_io import PWM,Servo,I2C
import cv2
import os

import sys
import tty
import termios

# region  read keyboard 
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
    S: right
    D: down
    Q: take photo

    G: Quit
'''
# endregion

# # check dir 
def check_dir(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception as e:
            print(e)

I2C().reset_mcu()
sleep(0.01)

pan = Servo(PWM("P1"))
tilt = Servo(PWM("P0"))
pan.angle(0)
tilt.angle(0)
panAngle = 0
tiltAngle = 0

'''
    https://docs.opencv.org/3.4.15/d2/d8d/classcv_1_1Stitcher.html
    https://github.com/opencv/opencv/blob/4.2.0/samples/python/stitching.py
    https://github.com/opencv/opencv/blob/4.2.0/samples/python/stitching_detailed.py

'''
Status_info = {
  0: 'OK',
  1: 'ERR_NEED_MORE_IMGS',
  2: 'ERR_HOMOGRAPHY_EST_FAIL',
  3: 'ERR_CAMERA_PARAMS_ADJUST_FAIL',
}

def panorama_shooting(path):
    global panAngle,tiltAngle

    temp_path = "/home/pi/picture/.temp/panorama"
    imgs =[]

    # check path
    check_dir(path)

    # stitcher = cv2.createStitcher(cv2.Stitcher_SCANS)
    stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
    
    # tilt.angle(0)
    # panAngle  = -90
    for a in range(panAngle,-91,-5):
        panAngle = a
        pan.angle(panAngle)
        sleep(0.1)
    # take photo
    num = 0
    for angle in range(-80,80,20):
        for a in range(panAngle,angle,1):
            panAngle = a
            pan.angle(a)
            sleep(0.1)
        sleep(0.5)
        # sleep(0.5)
        print(num,angle)
        Vilib.take_photo(photo_name='%s'%num,path=temp_path)
        sleep(0.2)
        num += 1

    # stitch image 
    for index in range(num):
        imgs.append(cv2.imread('%s/%s.jpg'%(temp_path,index)))
        cv2.imshow('test',imgs[index])
    print('imgs num: %s'%len(imgs))

    status,pano = stitcher.stitch(imgs)

    # imwrite and imshow
    print('status: %s , %s'%(status,Status_info[status]))
    if status == 0:
        cv2.imwrite('%s/%s.jpg'%(path,strftime("%Y-%m-%d-%H.%M.%S", localtime())),pano)
        cv2.imshow('panorama',pano)


    # clear temp
    # os.removedirs(temp_path)
    os.system('sudo rm -r %s'%temp_path)

# main

def main():

    Vilib.camera_start(inverted_flag=True)
    Vilib.display(local=True,web=False)

    path = "/home/pi/picture/panorama"
  
    print(manual)
    while True:
        key = readchar()
        # take photo
        if key == 'q': 
            print("panorama shooting ...")
            panorama_shooting(path)

        # esc
        if key == 'g':
            print('Quit')
            Vilib.camera_close()
            break 
    
        sleep(0.01)   

if __name__ == "__main__":
    main()