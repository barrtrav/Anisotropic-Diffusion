**Bibliotecas que se usaron:**

* os
* PIL
* sys
* time
* json
* math
* pylab
* numpy
* pickle 
* random
* pathlib
* threading
* collections
* scipy.ndimage
* multiprocessing
* skimage.feature
* scipy.cluster.vq
* skimage.segmentation 
* skimage.filters.edges

*Ejecuci\'on:*
Se incluyen dos arichivos ```exceute-linux.sh``` y ```execute-window.bat```. En dependencia 
del sistema operativo en que se encuentre se ejecuta el respectivo archivo, este primero limpia 
la carpeta de output y ejecuta ```python Experimentacion.py```. Las im\'agenes a procesar deben
ya estar dentro de la carpeta input. En la carpeta output se tiene 4 carpeta:

* logs: Donde se crea un *.txt* con toda la informaci\'on y tiempos de la ejecuci\'on.
* noisy: donde se almacenan las imagen original y la de bordes
* result: donde se almacena las im\'agenes resultante
* slic: donde se almacena las im\'agenes una vez realizada la segmentaci\'on

En el caso que se quiera probar alg\'un par\'ametro que no este incluido inicialmente
se modifican los valores de en el archivo Experimento:

* o: seria el filtro gaussiano usado.
* t: Cantidad de iteraciones.
* n_cluster: n\'umero de segmento, incluir valor dentro de array.
* kwep: bordes debiles, incluir valor dentro de array.
* ksep: bordes fuertes, incluir valor dentro de array.
* save_all: true si quieres guardar todas las iteraciones realizadas.