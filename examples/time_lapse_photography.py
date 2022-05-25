#!/usr/bin/env python3
'''
    Time-lapse photography based on the Raspistill command
'''
from time import time, sleep, strftime, localtime
from vilib import Vilib
import os
import sys
sys.path.append('./')
from servo import Servo
# import readchar
import cv2
import threading
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
    S: right
    D: down
    Q: start Time-lapse photography 
    E: stop
    G: Quit
'''
# endregion

# region servos init
pan = Servo(pin=13, min_angle=-90, max_angle=90) # pan_servo_pin (BCM)
tilt = Servo(pin=12, min_angle=-90, max_angle=30) # be careful to limit the angle of the steering gear
panAngle = 0
tiltAngle = 0
pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)

#endregion init

# # check dir 
def check_dir(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except Exception as e:
            print(e)

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

# endregion servo control

# Video synthesis
def video_synthesis(name:str,output:str,path:str,fps=30,format='.jpg',datetime=False):

    print('\nprocessing video, please wait ....')

    # video parameter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path+'/'+name+'.avi', fourcc, fps, (640,480))
    width = 640
    height = 480

    # traverse
   
    for root, dirs, files in os.walk(output):
        print('%s pictures need to be processed ...'%len(files))
        files = sorted(files)
        for file in files:
            # print('Format:',os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == format:
                # imread
                frame = cv2.imread(output+'/'+file)
                # add datetime watermark
                if datetime == True:
                    # print('name:',os.path.splitext(file)[1])
                    time = os.path.splitext(file)[0].split('-')
                    year = time[0]
                    month = time[1]
                    day = time[2]
                    hour = time[3]
                    minute = time[4]
                    second = time[5]
                    frame = cv2.putText(frame, 
                                        '%s.%s.%s %s:%s:%s'%(year,month,day,hour,minute,second),
                                        (width - 180, height - 25), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255),
                                        1, 
                                        cv2.LINE_AA)   # anti-aliasing
                # write video
                out.write(frame)

    # release the VideoWriter object
    out.release()
    # remove photos cache
    os.system('sudo rm -r %s'%output)
    print('\nDone.The video save as %s/%s'%(path,name))

# keyboard scan thread
key = None
breakout_flag=False
def keyboard_scan():
    global key
    while True:
        key = None
        key = readchar().lower()
        sleep(0.01)
        if breakout_flag==True:
            break
        
# continuous_shooting
def continuous_shooting(path, interval_s=3, duration_s=3600):
    print('\nStart time-lapse photography, press the "e" key to stop')   

    start_time = time()
    node_time = start_time

    while True: 
          
        if time()-node_time > interval_s:
            node_time = time()
            Vilib.take_photo(photo_name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),path=path)
        if key == 'e' or time()-start_time > duration_s:
            break
        sleep(0.01) # second


# main
def main():
    global key
    
    
    Vilib.camera_start(vflip=True,hflip=True)
    Vilib.display(local=True,web=True)

    sleep(2)
    print(manual)
    sleep(0.2)
    t = threading.Thread(target=keyboard_scan)
    t.setDaemon(True)
    t.start()
    
    path = "/home/pi/Videos/vilib/time_lapse"
    check_dir(path)

    while True:
        servo_control(key)

        # time-lapse photography
        if key == 'q':
            # check path
            output = path+'/'+strftime("%Y-%m-%d-%H-%M-%S", localtime())
            check_dir(output)
            # take a picture every 3 seconds for 3600 seconds
            continuous_shooting(output, interval_s=3, duration_s=3600)
            # video_synthesis
            name=strftime("%Y-%m-%d-%H-%M-%S", localtime())
            video_synthesis(name=name,
                            output=output,
                            path=path,
                            fps=30,
                            format='.jpg',
                            datetime=True)       
        # esc
        if key == 'g':
            Vilib.camera_close()
            global breakout_flag
            breakout_flag=True
            sleep(0.1)
            print('The program ends, please press CTRL+C to exit.')
            break 
        sleep(0.01)

if __name__ == "__main__":
    main()

    