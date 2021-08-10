import os
import pickle
import Diffusion
import QualityMeasure
import OpenImg as oim
import multiprocessing as mp

from numpy import copy
from time import clock
from pathlib import Path
from Utils import parametros
from Edges import edge_image
from pylab import imsave , gray
from scipy.ndimage import gaussian_filter

clock()
saver=False
debug=True
out=Path("./output/results")
noisy=Path("./output/noisy")

to_process=mp.Queue()

def apply_noise(gauss_filter):
    global to_process
    ok=True
    for img in oim.images:
        noisyname = str(noisy/img.name)[:-4]+" - noise"  #construir los nombres
        imagename = str(noisy/img.name)[:-4]+".jpg"
        noiseimagename = noisyname+'.jpg'
        toprocces = noisyname+'.pickled'
        toproccesoriginal = imagename[:-4]+'.pickled'
        toproccesoriginaledge = imagename[:-4]+'.pickledge'
        originaledge = imagename[:-4]+'_edge.jpg'
        to_process.put(toprocces) #agregar a la lista de procesamiento
         
        if os.path.exists(Path(toprocces)) and os.path.exists(Path(toproccesoriginal)) and os.path.exists(Path(toproccesoriginaledge)):
            print(f'- Existe: {toprocces}')
            continue
        
        Img = oim.read_image(img) #read the image
        print("Origen: "+imagename)
        edge_image(Img, toproccesoriginaledge, originaledge)
        nImg=gaussian_filter(Img, gauss_filter)
        try:
            gray()
            imsave(imagename,Img) #Saving the image
            imsave(noiseimagename,nImg) #and the noisy
            pickle.dump(nImg, open(Path(toproccesoriginal), 'wb'),4)
            pickle.dump(nImg, open(Path(toprocces), 'wb'),4)
            print(f'- Escrito: {toprocces}')
        except Exception as e:
            ok=False
            print(f'Error guardando imagenes con ruido\n {e}')
    print(f'Finalizando aplicacion de ruido. ---- {ok}')

def process(param, noiseimage, debug = False):
    global out
    if type(param)!=parametros:
        raise TypeError("param is not an Utils.parametros object")
    testcode=str(param)        
    print(f"- Processing: {noiseimage}\n    with: {testcode}\n")
    try:
        originalimage = noiseimage[:-16]+'.pickled' #direccion de la imagen original
        edgeimage = originalimage+'ge'
        nombre=Path(str(Path(originalimage).name)[:-8])
        salidafolder = out/nombre #carpeta de salida
        salidafolder.mkdir(exist_ok=True)
    except Exception as e:
        print(f'Error creando direcciones')
        return

    try:
        Img=pickle.load(open(noiseimage, 'rb'))
        p=salidafolder/Path(str(nombre)+testcode+'.pickled')
        j=str(salidafolder/Path(str(nombre)+testcode+'.jpg'))
    except Exception as e:
        print(f'Error leyendo imagen\n   {e}')
        a= input("Desea continuar 2 (y)es or (n)o?:   ")
        return
           
    try:
        time=clock()
        NewImg, NewImgNorm = Diffusion.ad_step_time_slic(Img, j[:-4], edgeimage, param, debug, nombre)
        print(f'\n- Tiempo de difusion {clock()-time} para {param.t} iteraciones')
    except Exception as e:
        print(f'Error procesando imagen\n    {e}')
        return
    
    if not saver:
        try:
            pickle.dump(NewImg, open(p, 'wb'),4, fix_imports=False)
            imsave(j,NewImg)
        except Exception as e:
            print(f'Error salvando la imagen\n    {e}')
            a= input("Desea continuar 4 (y)es or (n)o?:   ")
            return

#    aqui
#==============================================================================
#     #Estadisticas de calidad
#    qualitys=QualityMeasure.quality_measures(pickle.load(open(originalimage)),NewImg)
#    json.dump(qualitys,open(str(tpath/origin.name)[:-4]+testcode+".json","w"))
#    print("Finishing: "+str(nimg)+"\n    with: "+testcode+"\n")
#==============================================================================
