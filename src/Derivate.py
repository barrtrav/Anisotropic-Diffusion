import numpy as _np

dirX = [  0, 1, 0, -1 ]
dirY = [ -1, 0, 1,  0 ]

def in_range(x, y, img):
    return -1 < x < img.shape[0] and -1 < y < img.shape[1]

def derivate(direction, img):
    img_der = _np.zeros(img.shape)

    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            movX = x + dirX[direction]
            movY = y + dirY[direction]
            if(in_range(movX, movY, img)):
                img_der[x, y] = img[movX, movY] - img[x, y]

    return img_der

def derivateOpt(direction, img):
    a=direction.lower()
    res = img.copy()
    if a == 'n':
        res[:, :-1] -= img[:, 1:]
    elif a == 'w':
        res[:-1, :] -= img[1:, :]
    elif a == 's':
        res[:, 1:] -= img[:, :-1]
    elif a == 'e':
        res[1:, :] -= img[:-1, :]
    else:
        raise BaseException("Unknown Direction in derivateOpt")
    return res
