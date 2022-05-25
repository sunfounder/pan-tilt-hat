#!/usr/bin/env python3
from vilib import Vilib

def main():
    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)
    Vilib.image_classify_set_model(path='/home/pi/pan-tilt-hat/models/mobilenet_v1_0.25_224_quant.tflite')
    Vilib.image_classify_set_labels(path='/home/pi/pan-tilt-hat/models/labels_mobilenet_quant_v1_224.txt')
    Vilib.image_classify_switch(True)

if __name__ == "__main__":
    main()
    