import collections
from time import clock
from pylab import zeros, exp, imsave
import KMMC
from skimage.segmentation import slic
from multiprocessing import current_process

#****************************sin segmentacion*******************************#
def coef_e(img, db, bf):
    matrix_coef = zeros(img.shape)
    try:
        k = KMMC.kmmc(img, db, bf)
    except Exception as ef:
        print(f'Error calculando "k"\n    {ef}')
        return [[0]]
    k2 = k*k
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            exponent = -(img[x, y]**2 / k2)
            matrix_coef[x, y] = exp(exponent)

    return matrix_coef


#***********************CON SEGMENTACION SLIC********************************#


def in_range(x, y, img):
    return -1 < x < img.shape[0] and -1 < y < img.shape[1]

def segm_coef(img, db=0.1, bf=0.05, num_seg=30, debug = False, inittime=0, name=None):
    loggin=''

    labels = slic(img, num_seg ,multichannel=False)
    imsave(f'./output/slic/{name}_color_{db}_{bf}_{inittime}_{num_seg}.jpg', labels)
        
    #se crea la futura matriz de coeficientes
    matrix_coef = zeros(img.shape)

    #matriz de bool para saber cuando se proceso o no un pixel
    process = zeros(img.shape, dtype=bool)

    #calculo de los centroides globales con KMMC2
    extGlobals = KMMC.kmmc2(img, onlyKm=True)

    #recorriendo cada pixel
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            if not process[x, y]:
                superpixel = bfs_cluster(img, process, labels, (x, y), labels[x, y])

                k = KMMC.kmmc2(img, db, bf, superpixel=superpixel, extGlobal=extGlobals)

                for i in range(len(superpixel)):
                    pos = superpixel[i]
                    matrix_coef[pos] = -((img[pos] / k))**2 if k != 0 else 0
    
    imsave(f'./output/slic/{name}_white_{db}_{bf}_{inittime}_{num_seg}.jpg', matrix_coef)
    matrix_coef = exp(matrix_coef)
    imsave(f'./output/slic/{name}_black_{db}_{bf}_{inittime}_{num_seg}.jpg', matrix_coef)

    return matrix_coef, loggin

dirX = [0, 1, 0, -1]
dirY = [-1, 0, 1, 0]

def bfs_cluster(img, process, labels, pos, num_lbl):
    superpixel = []
    queue = collections.deque()
    queue.append(pos)
    process[pos] = True
    while len(queue) != 0:
        current = queue.popleft()
        for i in range(0, 4):
            adyX = current[0] + dirX[i]
            adyY = current[1] + dirY[i]
            if in_range(adyX, adyY, img) and not process[adyX, adyY] and labels[adyX, adyY] == num_lbl:
                queue.append((adyX, adyY))
                process[adyX, adyY] = True
        superpixel.append(current)

    return superpixel

