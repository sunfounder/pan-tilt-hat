Time Lapse Photography
======================

Some things happen too slowly for us to perceive, such as the legend of the flow of people, sunrise and sunset, and the blooming of flower buds. Time-lapse photography allows you to see these exciting things clearly.

You will use two windows at the same time in this project:
One is Terminal, where you will enter ``wasd`` to control the camera orientation, enter ``q`` to record, then enter ``e`` to stop, and enter ``g`` to exit shooting. If the program has not been terminated after exiting the shooting, please press ``ctrl+c``.
Another browser interface, after the program runs, you will need to enter ``http://<Your Raspberry Pi IP>:9000/mjpg`` in the PC browser (such as chrome) to view the screen.


.. raw:: html

    <iframe width="516" height="387" src="https://www.youtube.com/embed/Y19uTA079Z8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


**Run the Code**

.. raw:: html

    <run></run>

.. code-block::

    cd /home/pi/pan-tilt-hat/examples
    sudo python3 time_lapse_photography

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

.. image:: image/display.png


**Code**

.. code-block:: python

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


.. 5.31 mark

**How it works?**

Similar to :ref:`Continuous Shooting`, this example also needs to be split for analysis. It includes the following parts:

* Servo control
* Key input
* Path management
* Shooting
* Video synthesis

1. **Servo Control**: It is exactly the same as Continuous Shooting, no need to repeat it.

2. **Key input**: Its implementation is consistent with Continuous Shooting (ie ``readchar()``), but it is called by a separate thread. We extract the relevant code separately, as follows:

    .. code-block:: python

        '''
        Time-lapse photography based on the Raspistill command
        '''
        from time import sleep,

        import sys
        import tty
        import termios
        import threading

        # region  read keyboard 
        def readchar():
            pass

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
                
        # main
        def main():

            t = threading.Thread(target=keyboard_scan)
            t.setDaemon(True)
            t.start()
            
            while True:  
                # esc
                if key == 'g':
                    global breakout_flag
                    breakout_flag=True
                    sleep(0.1)
                    print('The program ends, please press CTRL+C to exit.')
                    break 
                sleep(0.01)

        if __name__ == "__main__":
            main()

    Simply put, the ``t = threading.Thread(target=keyboard_scan)`` line of the main function generates a thread and calls the ``keyboard_scan()`` function. This function calls ``readchar()`` in a loop until the ``breakout_flag`` ends after being modified.

    For details on the use of threads, please refer to `Threading - Python Docs <https://docs.python.org/3/library/threading.html?thread#threading.Thread>`_.

3. **Route Management**: Used to ensure that the file read and write path during shooting is correct. It includes the following:

    .. code-block:: python

        import os

        # # check dir 
        def check_dir(dir):
            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                except Exception as e:
                    print(e)

        # main
        def main():
            path = "/home/pi/Videos/vilib/time_lapse"
            check_dir(path)

            while True:
                if key == 'q':
                    #check path
                    output = path+'/'+strftime("%Y-%m-%d-%H-%M-%S", localtime())
                    check_dir(output)

                    # take_photo
                    # video_synthesis
                    

        if __name__ == "__main__":
            main()

    The target directory for our output videos is ``path``. And generating video requires a large number of temporary still photos, which are stored in ``output``. The function of ``check_dir()`` is to check whether the target folder exists, and create it if it does not exist.

    An ``os`` library is imported here, which allows python to use related functions of the operating system. Such as reading and writing files, creating files and directories, and manipulate paths. For details, please see `OS - Python Docs <https://docs.python.org/3/library/os.html>`_.

4. **Shooting**: Similar to :ref:`Continuous Shooting`, the difference is that instead of writing a specific number of photos, you manually press ``e`` to stop. This is achieved because the keyboard input is separated from the main program and runs on the thread separately.

    .. code-block:: python

        from time import time, sleep, strftime, localtime
        from vilib import Vilib

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

            Vilib.camera_start(vflip=True,hflip=True)
            Vilib.display(local=True,web=True)
            
            while True:
                # time-lapse photography
                if key == 'q':
                    #check path

                    # take a picture every 3 seconds for 3600 seconds
                    continuous_shooting(output, interval_s=3, duration_s=3600)
                    
                    # video_synthesis
                    
                # esc
                if key == 'g':
                    Vilib.camera_close()
                    break 
                sleep(0.01)

        if __name__ == "__main__":
            main()

5. **Video synthesis**: It uses the photos stored in the ``output`` path as frames, and generates a video output to the ``path``.

    .. code-block:: python

        from time import time, sleep, strftime, localtime
        from vilib import Vilib
        import cv2
        import os

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

        # main
        def main()
            while True:
                if key == 'q':
                    #check path
                    # take_photo
                    
                    # video_synthesis
                    name=strftime("%Y-%m-%d-%H-%M-%S", localtime())
                    video_synthesis(name=name,
                                    output=output,
                                    path=path,
                                    fps=30,
                                    format='.jpg',
                                    datetime=True)   
                    

        if __name__ == "__main__":
            main()


    Here, the video writer object is initialized first. The code show as below:

    .. code-block:: python

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output+'/'+name, fourcc, fps, (640,480))

    This module is derived from OpenCV, please refer to `VideoWriter-OpenCV Docs <https://docs.opencv.org/4.0.0/dd/d9e/classcv_1_1VideoWriter.html>`_ for details.

    Then, loop through each frame to form a video:

    .. code-block:: python

        for root, dirs, files in os.walk(input):
            print('%s pictures be processed'%len(files))
            files = sorted(files)
            for file in files:
                if os.path.splitext(file)[1] == format:
                    # imread
                    frame = cv2.imread(input+'/'+file)
                    # add datetime watermark
                    if datetime == True:
                        time = os.path.splitext(file)[0].split('-')
                        year = time[0]
                        month = time[1]
                        day = time[2]
                        hour = time[3]
                        minute = time[4]
                        second = time[5]
                        frame = cv2.putText(frame, '%s.%s.%s %s:%s:%s'%(year,month,day,hour,minute,second),
                                            (width - 180, height - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 255, 255),1,cv2.LINE_AA)   # anti-aliasing
                    # write video
                    out.write(frame)

    After the video is processed, release the VideoWriter.

    .. code-block:: python

        # release the VideoWriter object
        out.release()

    Finally delete the ``input`` folder. Of course, if you have enough space, comment out this line of code to keep the original picture.

    .. code-block:: python

        # remove photos cache
        os.system('sudo rm -r %s'%output)
        print('\nDone.The video save as %s/%s'%(path,name))