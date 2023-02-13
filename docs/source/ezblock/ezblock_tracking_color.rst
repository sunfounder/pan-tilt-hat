Color Tracking
==============

Prepare a small red ball and place it directly in front of the camera of Pan-Tilt HAT. The camera can consistently track the ball. This project may be little harder than the previous projects.


.. image:: img/IMG_0466.jpg

**TIPS**

Mathematical operation block can perform "+ , - , x , ÷".

.. image:: img/sp211112_110105.png

This block is often used together with variables to limit their ranges.

.. image:: img/sp211112_110828.png

You can get the information of detected color through this block. Modify the drop-down menu options, and choose to read the coordinates, size or number.

.. image:: img/sp211112_110909.png

The “object detection” can output the detected coordinate value (x, y) based on the center point of the graphic. The screen is divided into a 3x3 grid, as shown on the left.

.. image:: img/sp211112_111146.png

The “object detection” can detect the size (Width & Height) of the graphic. 

.. image:: img/sp211112_111229.png


.. note::In the above two usages, if multiple targets are identified, the largest target will be the sole result.


**EXAMPLE**

.. image:: img/sp211112_103737.png