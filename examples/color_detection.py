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

