import Derivate
import coefficient

from pylab import imsave, gray #, bone
from numpy import zeros, copy
from multiprocessing import current_process, Pool
from os import cpu_count
from pickle import dump as pdump
from pickle import load
from time import clock
from Edges import  edge_image
from QualityMeasure import quality_measures
import json
import sys

def anisotropic_diffusion_nixon(img, h, bd=0.1, bf=0.05):
    imgR = zeros(img.shape)

    dN = Derivate.derivateOpt("n", img)
    cN = coefficient.coef_e(dN, bd, bf)
    if len(cN)==1:
        return [[0]]

    dW = Derivate.derivateOpt("w", img)
    cW = coefficient.coef_e(dW, bd, bf)
    if len(cW)==1:
        return [[0]]
    dS = Derivate.derivateOpt("s", img)
    cS = coefficient.coef_e(dS, bd, bf)
    if len(cS)==1:
        return [[0]]
    dE = Derivate.derivateOpt("e", img)
    cE = coefficient.coef_e(dE, bd, bf)
    if len(cE)==1:
        return [[0]]
    imgR = img + ((cN*dN + cW*dW + cS*dS + cE*dE) * h)
    return imgR

def anisotropic_diffusion_nixon_slic(img, h, upbd=0.1, updf=0.05, num_seg=30,debug=False, name=None):
    imgR = zeros(img.shape)

    bd = upbd
    bf = updf
    
    cpus=cpu_count()
    if cpus>=4:
        cpus=4
    
    time=clock()
    MyPool= Pool(cpus, maxtasksperchild=1)
    directions=MyPool.starmap(Derivate.derivateOpt,[('n', img),('w', img),('s', img),('e', img)])
    print(f'--- Tiempo en las derivadas  {clock()-time}\n')
    MyPool.close()
    
    time=clock()
    MyPool= Pool(cpus, maxtasksperchild=1)
    time=clock()
    coeficientes = MyPool.starmap(coefficient.segm_coef,[(directions[0], bd, bf, num_seg, debug, time, name),(directions[1], bd, bf, num_seg, debug, time, name),(directions[2], bd, bf, num_seg, debug,time, name),(directions[3], bd, bf, num_seg, debug,time, name)])
    MyPool.close()
    print(f'--- Tiempo en los coeficientes  {clock()-time}\n')
    
    time=clock()
    imgR = img + ( ( coeficientes[0][0]*directions[0] + coeficientes[1][0]*directions[1] + coeficientes[2][0]*directions[2] + coeficientes[3][0]*directions[3] )  * h)
    print(f'--- Tiempo en creando nueva imagen  {clock()-time}\n')
    print(coeficientes[0][1]+coeficientes[1][1]+coeficientes[2][1]+coeficientes[3][1])

    return imgR

def ad_step_time_slic(img, name, edgeimage, param, debug=False, imname=None):
    img_t = copy(img)
    img_normal = copy(img)
    error_normal = False
    gray()
    try:
        edge_original = load(open(edgeimage, "rb"))
    except Exception as ef:
        print(f'Error cargando los bordes\n    {ef}')
        sys.exit()    
    for i in range(param.t):
        time=clock()
        img_t = anisotropic_diffusion_nixon_slic(img_t, param.h, param.updb, param.upbf, param.num_seg, debug, imname)
        print(f'\n-- Tiempo en Nixon_Slic  {clock()-time}')
        if not error_normal:
            time=clock()
            img_normal = anisotropic_diffusion_nixon(img_normal, param.h, param.updb, param.upbf)
            if len(img_normal) != 1:
                error_normal = False
            else:
                error_normal = True
            print(f'\n-- Tiempo en Nixon_Normal  {clock()-time}')
        if param.saver:
            rname=name[:-1]
            if param.t>9:
                rname=rname[:-1]
            rname=rname + f'{i+1}'
            pdump(img_t, open(rname+'.pickled','wb', 4))
            imsave(rname+".jpg", img_t)
            edge_t = edge_image(img_t, rname+'.pickledge', rname+'_edge.jpg')
            if not error_normal:
                pdump(img_normal, open(rname+'.normpickled','wb', 4))
                imsave(rname+"_norm.jpg", img_normal)
                edge_normal = edge_image(img_normal, rname+'_norm.pickledge', rname+'_norm_edge.jpg')
            print("Terminando de guardar imagenes nuevas")


            qm_t = quality_measures(edge_original,edge_t)
            json.dump(qm_t,open(rname+'.json',"w"))
            if not error_normal:
                qm_normal = quality_measures(edge_original,edge_normal)
                json.dump(qm_normal,open(rname+'_norm.json',"w"))

    return (img_t, img_normal)