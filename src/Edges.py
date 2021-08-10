import json
import pickle
# import OpenImg
import QualityMeasure

from numpy import abs
from pathlib import Path
from pylab import imsave, gray
from skimage.feature import canny
from skimage.filters.edges import sobel, prewitt, scharr

noisy=Path("./noisy")

def edge_image(img, p_e, j_e):

    try:
        ed = abs(scharr(img))
        print(p_e, j_e)
        pickle.dump(ed, open(p_e, 'wb'), 4, fix_imports=False)
        gray()
        imsave(j_e, ed)
    except:
        return 0
    return ed

def avisa():
    from winsound import Beep
    for i in range(1000):
        Beep(1000, 500)
        Beep(1000, 1000)
        Beep(1000, 500)
        Beep(1000, 500)
        Beep(20000, 1000)
        Beep(1000, 500)
        Beep(1000, 1000)

def dfdfsdf(inpu=[Path("./results")]):
    for i in inpu:
        imagess = [x for x in i.rglob('*.pickled')]
        for img in imagess:
            name = str(img.name).split(sep='-')[0]
            IMG = pickle.load(open(img, 'rb'))
            j_e = str(img)[:-8]+'_edge.jpg'
            p_e = str(img)+"ge"
            edge_image(IMG, p_e, j_e)
            qualitys=QualityMeasure.quality_measures(pickle.load(open(noisy/str(name+".pickledge"),'rb')),IMG)
            json.dump(qualitys,open(str(img)[:-8]+'.json',"w"))

if __name__ == "__main__":
    dfdfsdf()
    avisa()
