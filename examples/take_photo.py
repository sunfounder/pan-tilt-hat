from vilib import Vilib

def main():

    Vilib.camera_start(vflip=True,hflip=True) 
    Vilib.display(local=True,web=True)

    path = "/home/pi/Pictures/"
  
    while True:
        key = input()
        if key == "q":
            Vilib.take_photo(photo_name="new_photo",path=path)
            print("Take Photo")
        if key == "g":
            Vilib.camera_close()
            break 
            
if __name__ == "__main__":
    main()