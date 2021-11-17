Color Detection
===============

Say a color and mark it in the field of view. This is not difficult for most humans, because we have been trained in this way since we were young.

For computers, thanks to deep learning, such tasks can also be accomplished. In this project, there is an algorithm that can find a certain color (6 kinds in total), such as finding "orange".


.. image:: image/sp211116_105443.png

**Run the Code**

.. raw:: html

    <run></run>

.. code-block::

    cd /home/pi/pan-tilt-hat/examples
    sudo python3 color_detection.py

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

Then you can enter ``http://<your IP>:9000/mjpg`` in the browser to view the video screen. such as:  ``https://192.168.18.113:9000/mjpg``

.. image:: image/display.png

**Call the Function**

After the program runs, you will see the following information in the final:

.. code-block::

    Input key to call the function!
    q: Take photo
    1: Color detect : red
    2: Color detect : orange
    3: Color detect : yellow
    4: Color detect : green
    5: Color detect : blue
    6: Color detect : purple
    0: Switch off Color detect
    s: Display detected object information


Please follow the prompts to activate the corresponding functions.


    *  **Color Detect**

        Entering a number between ``1~6`` will detect one of the colors in "red, orange, yellow, green, blue, purple". Enter ``0`` to turn off color detection.

        .. image:: image/DTC2.png

        .. note:: You can download and print the :download:`PDF Color Cards <https://github.com/sunfounder/sf-pdf/raw/master/prop_card/object_detection/color-cards.pdf>` for color detection.

   
    *  **Display Information**

        Entering ``s`` will print the information of the color detection target in the terminal. Including the center coordinates (X, Y) and size (Weight, height) of the measured object.


**Code** 

.. code-block:: python

    from vilib import Vilib

    flag_color = False

    manual = '''
    Input key to call the function!
        q: Take photo
        1: Color detect : red
        2: Color detect : orange
        3: Color detect : yellow
        4: Color detect : green
        5: Color detect : blue
        6: Color detect : purple
        0: Switch off Color detect
        s: Display detected object information
    '''

    def color_detect(color):
        print("detecting color :" + color)
        Vilib.color_detect(color)

    def show_info():
        if flag_color is True and Vilib.detect_obj_parameter['color_n']!=0:
            color_coodinate = (Vilib.detect_obj_parameter['color_x'],Vilib.detect_obj_parameter['color_y'])
            color_size = (Vilib.detect_obj_parameter['color_w'],Vilib.detect_obj_parameter['color_h'])
            print("Coordinate:",color_coodinate,"Size",color_size)

    def main():
        Vilib.camera_start(vflip=True,hflip=True) 
        Vilib.display(local=True,web=True)
        print(manual)

        global flag_color

        while True:
            key = input()  
            if key == "1":
                color_detect("red")
                flag_color = True
            elif key == "2":
                color_detect("orange")
                flag_color = True
            elif key == "3":
                color_detect("yellow")
                flag_color = True
            elif key == "4":
                color_detect("green")
                flag_color = True
            elif key == "5":
                color_detect("blue")
                flag_color = True
            elif key == "6":
                color_detect("purple")
                flag_color = True
            elif key =="0":
                Vilib.color_detect_switch(False)
                flag_color = False
            elif key == "s":
                show_info()

    if __name__ == "__main__":
        main()





**How it works?**

The first thing you need to pay attention to here is the following function. These two functions allow you to start the camera.

.. code-block:: python

    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)

Functions related to "color detection":

* ``Vilib.color_detect(color)`` : For color detection, only one color detection can be performed at the same time. The parameters that can be input are: ``"red"``, ``"orange"``, ``"yellow"``, ``"green"``, ``"blue"``, ``"purple"``
* ``Vilib.color_detect_switch(False)`` : Switch OFF color detection

The information detected by the target will be stored in the ``detect_obj_parameter = Manager().dict()`` dictionary.

In the main program, you can use it like this:

.. code-block:: python

    Vilib.detect_obj_parameter['color_x']

The keys of the dictionary and their uses are shown in the following list:

* ``color_x``: the x value of the center coordinate of the detected color block, the range is 0~320
* ``color_y``: the y value of the center coordinate of the detected color block, the range is 0~240
* ``color_w``: the width of the detected color block, the range is 0~320
* ``color_h``: the height of the detected color block, the range is 0~240
* ``color_n``: the number of detected color patches


