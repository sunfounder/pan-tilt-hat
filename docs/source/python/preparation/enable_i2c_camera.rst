Enable I2C and Camera Interface
========================================

Here we are using the Raspberry Pi's I2C and Camera interfaces, but by default they are disabled, so we need to enable them first.

#. Input the following command:

    .. raw:: html

        <run></run>

    .. code-block:: 

        sudo raspi-config

#. Choose **3** **Interfacing Options** by press the down arrow key on your keyboard, then press the **Enter** key.

    .. image:: media/image282.png
        :align: center

#. Then **P5 I2C**.

    .. image:: media/image283.png
        :align: center

#. Use the arrow keys on the keyboard to select **<Yes>** -> **<OK>** to complete the setup of the I2C.

    .. image:: media/image284.png
        :align: center

#. Go to **3 Interfacing Options** again and select **P1 Camera**.

    .. image:: media/camera_enable.png
        :align: center

#. Again select **<Yes>** -> **<OK>** to complete the setup.

    .. image:: media/camera_enable1.png
        :align: center

#. After you select **<Finish>**, a pop-up will remind you that you need to reboot for the settings to take effect, select **<Yes>**.

    .. image:: media/camera_enable2.png
        :align: center