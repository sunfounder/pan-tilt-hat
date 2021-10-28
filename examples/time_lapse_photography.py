'''
    Time-lapse photography based on the Raspistill command
'''
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
    Q: start/stop Time-lapse photography 

    G: Quit
'''
# endregion

# region init
I2C().reset_mcu()
sleep(0.01)

pan = Servo(PWM("P1"))
tilt = Servo(PWM("P0"))
panAngle = 0
tiltAngle = 0

pan.angle(0)
tilt.angle(0)

vflip = True  # -vf
hflip = False # -hf
output = "/home/pi/picture/time_lapse" # -o
timelapse = 3000    # -tl  /ms

# endregion

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
        tiltAngle = limit(tiltAngle, -90, 90)
        tilt.angle(tiltAngle)
    if key == 's':
        tiltAngle += 1
        tiltAngle = limit(tiltAngle, -90, 90)
        tilt.angle(tiltAngle)
    if key == 'a':
        panAngle += 1
        panAngle = limit(panAngle, -90, 90)
        pan.angle(panAngle)
    if key == 'd':
        panAngle -= 1
        panAngle = limit(panAngle, -90, 90)
        pan.angle(panAngle)

# endregion servo control

# Video synthesis
def video_synthesis(name:str,input:str,output:str,fps=30,format='.jpg',datetime=False):
    # video parameter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output+'/'+name, fourcc, fps, (640,480))
    width = 640
    height = 480

    # traverse
    for root, dirs, files in os.walk(input):
        for file in files:
            print('Format:',os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == '.'+ format:
                # imread
                frame = cv2.imread(input+file)
                # add datetime watermark
                if datetime == True:
                    print('name:',os.path.splitext(file)[1])
                    time = os.path.splitext(file)[0].split('-')
                    year = time[0]
                    month = time[0]
                    day = time[0]
                    hour = time[0]
                    minute = time[0]
                    second = time[0]
                    frame = cv2.putText(frame, 
                                        '%s.%s.%s %s:%s:%s'%(year,month,day,hour,minute,second),
                                        (width - 120, height - 25), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                        (255, 255, 255),
                                        1, 
                                        cv2.LINE_AA)   # anti-aliasing
                # write video
                out.write(frame)

    # release the VideoWriter object
    out.release()

    
# main
def main():

    Vilib.camera_start(inverted_flag=True)
    Vilib.display(local=True,web=True)
  
    print(manual)
    while True:
        key = readchar()
        # servo control
        # servo_control(key)
        # time-lapse photography
        if key == 'q':
            input = output+'/'+strftime("%Y-%m-%d-%H-%M-%S", localtime())
            check_dir(input)
            check_dir(output)

            #  take_photo
            count = 0
            delay = 100 # ms
            print('start time-lapse photography, press the "q" key to stop')
            Vilib.take_photo(photo_name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),path=input)        
            while True:
                print('count:%s'%count)
                if count == timelapse/delay:
                    count = 0
                    Vilib.take_photo(photo_name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),path=input)
                
                key = readchar()
                if key == 'q':
                    break

                count += 1
                sleep(delay/1000) # second
            # video_synthesis
            print('processing video, please wait ....')
            video_synthesis(name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),
                            input=input,output=output,fps=30,format='.jpg',datetime=True)
            # remove photos
            os.removedirs(input)
            print('Done.The video save as %s'%output)

        # esc
        if key == 'g':
            Vilib.camera_close()
            break 
    
        sleep(0.01)

if __name__ == "__main__":
    main()