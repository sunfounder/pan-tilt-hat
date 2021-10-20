from vilib import Vilib

def main():
    Vilib.camera_start(inverted_flag=True)
    Vilib.display(local=True,web=True)
    # Vilib.image_classify_set_model(path='/opt/vilib/mobilenet_v1_0.25_224_quant.tflite')
    # Vilib.image_classify_set_labels(path='/opt/vilib/labels_mobilenet_quant_v1_224.txt')
    Vilib.image_classify_switch(True)

if __name__ == "__main__":
    main()