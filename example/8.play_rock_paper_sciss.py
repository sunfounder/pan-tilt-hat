#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
from ezblock import WiFi
import random
from ezblock import print
from ezblock import delay

randomNum = None
randomGes = None
detectedGes = None
ges1 = None
ges2 = None
ges3 = None
game = None

Vilib.camera_start(True)
Vilib.gesture_detect_switch(True)
WiFi().write('CN', 'MakerStarsHall', 'sunfounder')
game = 'over'

"""Describe this function...
"""
def getRandomGes():
    global randomNum,  randomGes,   detectedGes, ges1, ges2, ges3,game
    randomNum = random.randint(1, 3)
    if randomNum == 1:
        randomGes = 'rock'
    elif randomNum == 2:
        randomGes = 'scissor'
    else:
        randomGes = 'paper'

"""Describe this function...
"""
def detectGes():
    global randomNum, ges1, randomGes, game, ges2, detectedGes, ges3
    ges1 = Vilib.gesture_detect_object('type')
    delay(50)
    ges2 = Vilib.gesture_detect_object('type')
    delay(50)
    ges3 = Vilib.gesture_detect_object('type')
    if ges1 == ges2 and ges1 == ges3:
        detectedGes = ges1
    else:
        detectedGes = 'none'


def forever():
    global randomNum, ges1, randomGes, game, ges2, detectedGes, ges3
    if game == 'over':
        getRandomGes()
        game = 'start'
        print("%s"%'Ready? show your gesture!')
        delay(2000)
    detectGes()
    if detectedGes != 'none':
        print("%s"%detectedGes)
        if detectedGes == randomGes:
            print("%s"%'a draw')
        elif detectedGes == 'rock' and randomGes == 'scissor':
            print("%s"%'You win')
        elif detectedGes == 'scissor' and randomGes == 'paper':
            print("%s"%'You win')
        elif detectedGes == 'paper' and randomGes == 'rock':
            print("%s"%'You win')
        else:
            print("%s"%'You fail')
        game = 'over'
        detectedGes = 'none'
        delay(1000)

if __name__ == "__main__":
    while True:
        forever()  