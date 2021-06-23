from scipy.cluster.vq import whiten, kmeans, vq
from numpy import zeros, array, where
from math import log

def toArray(img):
    arrayPix = zeros((img.shape[0] * img.shape[1], 1))
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            posLineal = img.shape[1]*x + y
            arrayPix[posLineal, 0] = img[x, y]
    return arrayPix


def kmmc(img, updb, upbf):
    pixArray = toArray(img)

    minim = min(pixArray)[0]
    maxim = max(pixArray)[0]
    med = (minim + maxim) / 2

    projected = whiten(pixArray)
    cent = whiten([[minim], [med], [maxim]])
    centroids, distortion = kmeans(projected, cent)
    code, distance = vq(projected, centroids)

    minVal = []
    for c in range(3):
        ind = where(code == c)[0]
        minVal.append(min(ind))

    minVal.remove(min(minVal))
    minVal.sort()

    bdLn = log(updb) * (minVal[0]**2)
    bfLn = log(upbf) * (minVal[1]**2)
    sum_i = (minVal[0])**4 + (minVal[1])**4

    k = (-sum_i / (bdLn + bfLn))**0.5
    return k

#**************************************para el slic***********************************#
def listToArray(superpixel, img):
    if(len(superpixel) == 0):
        return toArray(img)

    arrayPix = zeros((len(superpixel), 1))
    for x in range(0, len(superpixel)):
        arrayPix[x, 0] = img[superpixel[x]]
    return arrayPix


def kmmc2(img, upbd=0.1, upbf=0.05, superpixel=[], onlyKm=False, extGlobal=[]):
    #se crea un array con todos los pixeles a procesar
    pixArray = listToArray(superpixel, img)

    #se determinan el maximoy el minimo de las intensidades
    minim = min(pixArray)[0]
    maxim = max(pixArray)[0]
    #se almacena el centroide inicial
    centroids = [[minim]]

    EPS = 1e-150
    #si la diferencia de intensidades no es infinitesimal se
    #aplica kmeans para k=2
    if EPS < maxim - minim:
        projected = whiten(pixArray)

        minim = array([min(projected)[0]])
        maxim = array([max(projected)[0]])

        init_cent = array([minim, maxim])
        centroids, distortion = kmeans(projected, init_cent)

    if onlyKm:
        return centroids

    k = _MC(centroids, upbd, upbf, extGlobal)
    return k

def _MC(centroids, updb, upbf, extGlobal):
    if len(centroids) == 1:
        ##se acerca mas al cjto min
        umbral = updb if abs(extGlobal[0] - centroids[0][0]) < abs(extGlobal[1] - centroids[0][0]) else upbf

        i = -(centroids[0][0])**2
        Ln = log(umbral) #COMPARO MIN O MAX LOCAL CON GLOBAL PARA VER CON Q UMBRAL COMP.
        k = (i/Ln)**0.5
        return k

    bdLn = log(updb) * (centroids[0][0]**2)
    bfLn = log(upbf) * (centroids[1][0]**2)
    sum_i = (centroids[0][0])**4 + (centroids[1][0])**4

    k = (-sum_i / (bdLn + bfLn))**0.5
    return k
