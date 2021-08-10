import threading as _th

from PIL import Image
from pathlib import Path
from pylab import array,gray

extensions=[".pgm", ".png", ".jpg", "bmp"]
inputs=[Path("./input")]
images=[]

reading=_th.Lock()

def read_image(path):
    with reading:
        img = array(Image.open(path).convert('L'),dtype='float64')
    gray()
    return img

def is_image(path):
    global extensions
    for i in extensions:
        if path.endswith(i):
            return True
    return False

def load_images(inpu=inputs):
    global extensions, inputs, images
    for i in inpu:
        images+=[x for x in i.rglob("*") if is_image(x.name)]
