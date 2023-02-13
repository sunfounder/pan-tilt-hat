Record Video
============

This example allows us to record a video.

Here you will use two windows at the same time:
One is Terminal, you can type ``wasd`` here to control the orientation of the camera, type ``q`` to record/pause/continue recording, type ``e`` to stop recording, and type ``g`` to exit shooting . If the program has not been terminated after exiting the shooting, please type ``ctrl+c``.
Another browser interface, after the program runs, you will need to enter ``http://<Your Raspberry Pi IP>:9000/mjpg`` in the PC browser (such as chrome) to view the viewfinder screen.


**Run the Code**

.. raw:: html

    <run></run>

.. code-block::

    cd /home/pi/pan-tilt-hat/examples
    sudo python3 record_video.py

**View the Image**

After the code runs, the terminal will display the following prompt:

.. code-block::

    No desktop !
    * Serving Flask app "vilib.vilib" (lazy loading)
    * Environment: production
    WARNING: Do not use the development server in a production environment.
    Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://0.0.0.0:9000/ (Press CTRL+C to quit)

Then you can enter ``http://<your IP>:9000/mjpg`` in the browser to view the video screen. such as:  ``http://192.168.18.113:9000/mjpg``

.. image:: img/display.png


**Code**

.. code-block:: python

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
        S: right
        D: down
        Q: record/pause/continue
        E: stop
        G: Quit
    '''

    # region init
    pan = Servo(pin=13, min_angle=-90, max_angle=90) # pan_servo_pin (BCM)
    tilt = Servo(pin=12, min_angle=-90, max_angle=30) # be careful to limit the angle of the steering gear
    panAngle = 0
    tiltAngle = 0
    pan.set_angle(panAngle)
    tilt.set_angle(tiltAngle)

    Vilib.rec_video_set["path"] = "/home/pi/Videos/vilib/" # set path
    vname = None
    rec_flag = 'stop' # start,pause,stop
    #endregion init

    # rec control
    def rec_control(key):
        global rec_flag, vname

        # start,pause
        if key == 'q':
            key = None
            if rec_flag == 'stop':            
                rec_flag = 'start'
                # set name
                vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                Vilib.rec_video_set["name"] = vname
                # start record
                Vilib.rec_video_run()
                Vilib.rec_video_start()
                print('rec start ...')
            elif rec_flag == 'start':
                rec_flag = 'pause'
                Vilib.rec_video_pause()
                print('pause')
            elif rec_flag == 'pause':
                rec_flag = 'start'
                Vilib.rec_video_start()
                print('continue')
        # stop       
        elif key == 'e' and rec_flag != 'stop':
            key = None
            rec_flag = 'stop'
            Vilib.rec_video_stop()
            print("The video saved as %s%s.avi"%(Vilib.rec_video_set["path"],vname),end='\n')  

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


    def main():

        Vilib.camera_start(vflip=True,hflip=True) 
        Vilib.display(local=True,web=True)
        sleep(2)
        print(manual)
        while True:
            key = readchar().lower()
            # rec control
            rec_control(key)
            # servo control
            servo_control(key)
            # esc
            if key == 'g':
                Vilib.camera_close()
                break 

            sleep(0.1)

    if __name__ == "__main__":
        main()


**How it works?**


This article can be divided into three parts to analyze:

* Keyboard input
* Servo control
* Record video

The first two parts are consistent with :ref:`Continuous Shooting`. The record video function code is as follows:

.. code-block:: python

    from time import sleep,strftime,localtime
    from vilib import Vilib

    # region init
    Vilib.rec_video_set["path"] = "/home/pi/Videos/vilib/" # set path
    vname = None
    rec_flag = 'stop' # start,pause,stop
    # endregion init

    # rec control
    def rec_control(key):
        global rec_flag, vname

        # start,pause
        if key == 'q':
            key = None
            if rec_flag == 'stop':            
                rec_flag = 'start'
                # set name
                vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                Vilib.rec_video_set["name"] = vname
                # start record
                Vilib.rec_video_run()
                Vilib.rec_video_start()
                print('rec start ...')
            elif rec_flag == 'start':
                rec_flag = 'pause'
                Vilib.rec_video_pause()
                print('pause')
            elif rec_flag == 'pause':
                rec_flag = 'start'
                Vilib.rec_video_start()
                print('continue')
        # stop       
        elif key == 'e' and rec_flag != 'stop':
            key = None
            rec_flag = 'stop'
            Vilib.rec_video_stop()
            print("The video saved as %s%s.avi"%(Vilib.rec_video_set["path"],vname),end='\n')  


    def main():

        Vilib.camera_start(vflip=True,hflip=True) 
        Vilib.display(local=True,web=True)

        while True:
            key = readchar().lower()
            # rec control
            rec_control(key)
            # servo control
            
            # esc
            if key == 'g':
                Vilib.camera_close()
                break 

    if __name__ == "__main__":
        main()

Parameters related to recording include the following:

* ``Vilib.rec_video_set["path"]`` ：The address where the video is saved
* ``Vilib.rec_video_set["name"]`` ：The name of the saved video

Functions related to recording include the following:

* ``Vilib.rec_video_run()`` ：Start recording
* ``Vilib.rec_video_pause()`` ：Pause recording
* ``Vilib.rec_video_start()`` ：Continue recording
* ``Vilib.rec_video_stop()`` ：Stop recording