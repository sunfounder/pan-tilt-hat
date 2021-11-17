
from time import sleep
from sunfounder_io import PWM,Servo,I2C


# region init
I2C().reset_mcu()
sleep(0.01)

pan = Servo(PWM("P1"))
tilt = Servo(PWM("P0"))
panAngle = 0
tiltAngle = 0
pan.angle(panAngle)
tilt.angle(tiltAngle)
# endregion init


def main():
    pass

if __name__ == "__main__":
    main()