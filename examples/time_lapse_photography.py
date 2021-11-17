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
import threading

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
    Q: start Time-lapse photography 
    E: stop
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
pan.angle(panAngle)
tilt.angle(tiltAngle)

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

    print('processing video, please wait ....')

    # video parameter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output+'/'+name, fourcc, fps, (640,480))
    width = 640
    height = 480

    # traverse
   
    for root, dirs, files in os.walk(input):
        print('%s pictures be processed'%len(files))
        files = sorted(files)
        for file in files:
            # print('Format:',os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == format:
                # imread
                frame = cv2.imread(input+'/'+file)
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

    # remove photos
    os.system('sudo rm -r %s'%input)
    print('Done.The video save as %s/%s'%(output,name))

# keyboard scan thread
key = None
breakout_flag=False
def keyboard_scan():
    global key
    while True:
        key = None
        key = readchar()
        sleep(0.01)
        if breakout_flag==True:
            break
        
# continuous_shooting
def continuous_shooting(path,interval_ms:int=3000):
    print('Start time-lapse photography, press the "e" key to stop')   

    delay = 10 # ms

    count = 0
    while True:    
        if count == interval_ms/delay:
            count = 0
            Vilib.take_photo(photo_name=strftime("%Y-%m-%d-%H-%M-%S", localtime()),path=path)
        if key == 'e':
            break
        count += 1
        sleep(delay/1000) # second


# main
def main():

    print(manual)

    Vilib.camera_start(vflip=True,hflip=True)
    Vilib.display(local=True,web=True)

    sleep(1)
    t = threading.Thread(target=keyboard_scan)
    t.setDaemon(True)
    t.start()
    
    
    while True:
        servo_control(key)

        # time-lapse photography
        if key == 'q':

            #check path
            output = "/home/pi/Pictures/time_lapse" # -o
            input = output+'/'+strftime("%Y-%m-%d-%H-%M-%S", localtime())
            check_dir(input)
            check_dir(output)

            # take_photo
            continuous_shooting(input,interval_ms=3000)
            
            # video_synthesis
            name=strftime("%Y-%m-%d-%H-%M-%S", localtime())+'.avi'
            video_synthesis(name=name,input=input,output=output,fps=30,format='.jpg',datetime=True)
            
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