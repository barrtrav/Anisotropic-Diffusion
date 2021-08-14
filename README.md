# Informe escrito

## Autores

| **Nombre(s) y Apellidos**  |              **Correo**              |                       **GitHub**                       |
| :------------------------: | :----------------------------------: | :----------------------------------------------------: |
| Reinaldo Barrera Travieso  |  r.barrera@estudiantes.matcom.uh.cu  |      [@Reinaldo14](https://github.com/Reinaldo14)      |
| Juan Carlos Esquivel Lamis | j.esquivel@estudiantes.matcom.uh.cu  | [@jesquivel960729](https://github.com/jesquivel960729) |
|    Ariel Plasencia Díaz    | a.plasencia@estudiantes.matcom.uh.cu |         [@ArielXL](https://github.com/ArielXL)         |

## Implementación y Ejecución

### Implementación

La parte computacional del proyecto está implementada completamente en [Python 3](https://es.wikipedia.org/wiki/Python). Python es un lenguaje de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código. Se trata de un lenguaje de programación multiparadigma, ya que soporta parcialmente la orientación a objetos, programación imperativa y, en menor medida, programación funcional. Es un lenguaje interpretado, dinámico y multiplataforma. Nos apoyamos en varias librerías provistas por dicho lenguaje de programación para una mejor y mayor comprensión en el código.

Para la instalación de las librerías ejecutamos el siguiente comando:

```bash
pip3 install -r requirements.txt
```

### Ejecución

Se incluyen dos archivos ```exceute-linux.sh``` y ```execute-window.bat```. En dependencia del sistema operativo en que se encuentre se ejecuta el respectivo fichero, este primero limpia la carpeta de output y ejecuta

```python
python3 Experimentacion.py
```

Las imágenes a procesar deben ya estar dentro de la carpeta input. En la carpeta output se tiene 4 carpeta:

* logs: donde se crea un archivo de texto con toda la información y tiempos de la ejecución.
* noisy: donde se almacenan las imagen original y la de bordes.
* result: donde se almacenan las imágenes resultantes.
* slic: donde se almacenan las imágenes una vez realizada la segmentación.

En el caso que se quiera probar algún parámetro que no este incluido inicialmente se modifican los valores en el fichero ```Experimento.py```:

* o: sería el filtro gaussiano usado.
* t: cantidad de iteraciones.
* n_cluster: número de segmento, incluir valor dentro de array.
* kwep: bordes débiles, incluir valor dentro de array.
* ksep: bordes fuertes, incluir valor dentro de array.
* save_all: true si quieres guardar todas las iteraciones realizadas.

## Resumen

En este trabajo se aplica el modelo de difusión anisotrópica de Perona-Malik a un conjuntos de imágenes de ultrasonidos. Para este proceso primero se particiona la imagen empleando una técnica de segmentación de superpíxeles, en este caso SLIC (Simple Liner Iterative Clustering). Una vez que son obtenidos estas regiones o segmentos se realiza un suavizado por regiones teniendo en cuenta la difusión anisotrópica que a diferencia de la isotrópica, esta permite conservar los bordes. También se discute un nuevo algoritmo para aproximar lo que se conoce como parámetro de constraste (k), el cual se emplea a la hora de obtener el coeficiente de difusión.

