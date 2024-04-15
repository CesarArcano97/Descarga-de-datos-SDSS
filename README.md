# Descarga de Archivos FITS y Datos Fotométricos del Sloan Digital Sky Survey (SDSS)

En este documento se detalla el proceso para descargar archivos FITS y datos fotométricos del [Sloan Digital Sky Survey (SDSS)](https://es.wikipedia.org/wiki/Sloan_Digital_Sky_Survey#:~:text=El%20Sloan%20Digital%20Sky%20Survey,M%C3%A9xico%20y%20comenzada%20en%202000.https://skyserver.sdss.org/dr12/en/home.aspx), una empresa astronómica que se ha destacado por su exhaustivo mapeo y catalogación de objetos extragalácticos.

El SDSS, iniciado en el año 2000, emplea un telescopio de 2.5 metros ubicado en Apache Point, Nuevo México. A lo largo de sus diversas fases, ha recopilado información diversa, incluyendo imágenes en formatos .jpg o .fits, espectros y datos fotométricos.

El Sloan tiene diferentes páginas para utilizarse, no entiendo muy bien por qué, pero a mi me gusta utilizar esta: [SkyServer SDSS](https://skyserver.sdss.org/dr12/en/home.aspx).

### Procedimiento de descarga

Para descargar datos del SDSS hay diferentes maneras de hacerlo, aquí veremos cómo bajar información fotométrica y archivos FITS a través de queries (solicitudes) en su plataforma de SQL (Structured Query Language). En caso de que no estén familiarizados con SQL, se trata de un lenguaje de programación diseñado para gestionar bases de datos y poder realizar descargas, actualizar tablas, o corregir información, entre otras cosas. 

La plataforma de búsqueda por SQL del Sloan se encuentra en la siguiente liga: [SQL search](https://skyserver.sdss.org/dr12/en/tools/search/sql.aspx). Una vez abierta la liga te vas a encontrar con una pantalla como la siguiente:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/1ca8a000-2fd0-4102-85f9-2fabfa40392e)


En el SQL Search del Sloan podrás ver algunas secciones, probablemente sea buena idea que te des una vuelta por ellas para que te des una idea de cómo es la plataforma. Sin embargo, hay una que dice SDDS Sample Queries Page, en la que encontrarás ejemplos de solicitudes SQL para que puedas bajar diferentes tipos de datos con distintas característicias. De igual forma, el SDSS tiene un curso para aprender SQL. No es necesario que lo sepas a la perfección, pero es buena idea echarle un ojo. 

Bueno, una vez en el SQL Search puedes comenzar a realizar solicitudes. La que viene predeterminada te devolverá algunas estrellas, galaxias y cuásares (QSO). Por cierto, en SQL utilizar "---" sirve para añadir comentarios al código.

```sql
-- La consulta selecciona las 10 primeras filas y ciertas columnas de las tablas PhotoObj y SpecObj.
SELECT TOP 10
   p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z,  -- Columnas de la tabla PhotoObj
   p.run, p.rerun, p.camcol, p.field,              -- Columnas adicionales de la tabla PhotoObj
   s.specobjid, s.class, s.z as redshift,         -- Columnas de la tabla SpecObj
   s.plate, s.mjd, s.fiberid                       -- Columnas adicionales de la tabla SpecObj
FROM PhotoObj AS p                                -- Alias 'p' para la tabla PhotoObj
   JOIN SpecObj AS s ON s.bestobjid = p.objid     -- Realiza una unión entre las tablas basada en la condición de igualdad de los IDs
WHERE 
   p.u BETWEEN 0 AND 19.6                          -- Restricción sobre la columna 'u' de la tabla PhotoObj
   AND g BETWEEN 0 AND 20                           -- Restricción sobre la columna 'g' de la tabla PhotoObj
```

Una vez creada tu solicitud, puedes dar clic en "Submit query" y eso te llevará a una pantalla como la siguiente:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/c3def354-90e5-4ecc-8a4d-fa446945190e)

Aquí ya empieza lo mero bueno. Esa tabla que se ve ahí contiene la información fotométrica solicitada en la query de SQL. Puedes ver que está "objiid" que es el id de cada objeto que le asignaron al momento de realizar la catalogación, están "run", "camcol", "plate" y otras cosas raras que puedes consultar en la documentación del SDSS. 

Probablemente lo más interesante en esta solicitud es la información de los "ugriz", los cuales son los filtros con los que el SDSS observa. El nombre ugriz viene dado por la longitud de onda que procesa cada uno de los filtros.

| Filtro                 | Longitud de onda Å |
| ---------------------- | ------------------ |
| u (ultravioleta)       | 2,534              |
| g (verde)              | 4,770              |
| r (rojo)               | 6,231              |
| i (infrarrojo cercano) | 7,625              |
| z (infarrojo)          | 9,134              |

Continuando, también verás información como la clasificación del objeto, las cuales están definidas en la columna "Class". Otros de los datos cruciales son "ra" y "dec", las coordenadas de cada objeto, que servirán para el recorte de las imágenes que posteriormente podrás utilizar en tus redes neuronales. 

Bueno, la manera en que yo guardo estas tablas de datos mostradas al dar clic en "Submit query" es simplemente seleccionandolas y pegándolas en una hoja de cálculo como la de excel o la de libre office. 

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/fd2cd280-5fdb-41bf-ad75-f0c6a88b7bf6)

En la hoja de calculo borro las columnas que no me sirven y listo. **Es importante que guardes las columnas antes de dar el siguiente paso**, que es solicitar los archivos FITS.

Muy bien, una vez con tu solicitud lo que sigue es dar clic en el botón de "Submit" mostrado después de "... FITS files:". Cuando le des clic ahí, verás una nueva pantalla, correspondiente al SAS. 

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/974b868f-379d-4c48-9aee-d53895ccd6e3)


Vas a bajar hasta la siguiente parte: 

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/29893df4-3437-4186-8636-c33f194116e2)

En ella puedes ver, de lado derecho, la fotografía del cielo en la que encontrarás los objetos solicitados. Como podrás notar, en la solicitud del SQL pedimos 10 objetos, y aquí solo se muestran siete imágenes. Esto sucede porque dentro de cada fotografía del cielo tomada por el SDSS puede haber uno o más objetos capturados.

Así se ve un FITS del SDSS:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/26230348-469d-4465-8669-94b3feab61a3)

Puedes ver cómo hay un montón de objetos por ahí volando.

Para descargar los FITS (estas fotografías del cielo), primero necesitas seleccionar el filtro de observación que prefieras. 

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/88a285a8-01e2-4881-a009-98849c427fe5)

Yo trabajé todo mi proyecto con fotografías en filtro verde, casi que de manera arbitraria. Se supone que el verde, al estar en el óptico, es bastante útil para estudiar estructuras de los objetos. Una investigación más en profundidad de lo que quieras hacer te ayudará a decidir qué filtro te conviene. 

Pero puedes hacer pruebas con el verde, así que nomás deja la "g" con una palomita.

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/4a059655-721d-4020-a344-d75a0d4037ff)

Lo siguiente es seleccionar todas las fotografías, dale al "All".

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/4bc8610f-bec9-4373-babf-df186c871698)

Ahora sí, le puedes dar al "Download FITS"

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/2e6d456c-145c-4818-a5aa-0cd9bd9c195b)

Eso abrirá un letrero:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/f44e2af3-5622-45e5-8533-8c4a8f857c77)

Este letrero te indica cómo debes bajar los datos. Volveremos a ello en un momento. Por ahora solo dale aceptar. Lo cual te abrirá lo siguiente:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/6ba1fc65-f869-4360-b701-78719a79cd4e)

El SDSS te proporcionará ligas para poder descargar cada FITS. Como para proyectos de aprendizaje automático son necesarios grandes volúmenes de datos, no solo siete viles fotografías, es natural pensar que no queremos descargar "a mano" cada imagen. Sería tardado y tedioso (de por si hasta ahora no ha sido la cosa más divertida del mundo). Entonces lo que haremos será guardar las ligas en un archivo ".txt" de tu bloc de notas. Copia y pega las ligas en el bloc. 

Aquí viene una de las cosas con las que sufrí para descargar los datos.

## Separador de ligas

Aquí viene el primer programa que deberás correr. 

El problema con las ligas que te da el SDSS es que vienen pegadas. Es decir, si tu copias y pegas las ligas, te quedarás con algo así:

https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/109/2/frame-g-000109-2-0037.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/109/4/frame-g-000109-4-0039.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/94/6/frame-g-000094-6-0094.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/109/1/frame-g-000109-1-0100.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/109/4/frame-g-000109-4-0149.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/109/4/frame-g-000109-4-0151.fits.bz2 https://dr12.sdss.org/sas/dr12/boss/photoObj/frames/301/94/6/frame-g-000094-6-0512.fits.bz2

Una sola liga unida que contiene a las siete diferentes ligas que te llevarán a cada FITS. Si le picas al vínculo verás que te marca un error. Entonces, cuando me tocó hacer esto pasé un muy, muy buen rato separando las ligas a mano. No sé cuántas veces tuve que dar "shift + enter" para separar miles de ligas. Hubo días que estuve hasta media hora, 45 min, separando ligas. 

Hasta que los dioses de la programación me iluminaron, y recurrí a automatizar la tarea. Si soy sincero, no era tan hábil programando cuando comencé a trabajar con José Antonio. Pero uno va aprendiendo. 

Puedes encontrar la rutina bajo el nombre de 'Separador.py' en los archivos del repositorio. El código separador de ligas es el siguiente:

```python
import re

# Ruta del archivo de entrada y salida
input_file_path = r"/home/cesar/Documentos/Recortes-prueba/datos-sdss-ligas.txt"
# Reemplaza "/ruta/a/la/carpeta/salida/salida.txt" con la ruta de la carpeta de salida deseada y el nombre del archivo de salida
output_file_path = r"/home/cesar/Documentos/Recortes-prueba/ligas-separadas.txt"

# Lee el contenido del archivo de entrada
with open(input_file_path, 'r') as file:
    input_text = file.read()

# Realiza la sustitución en el texto leído
output_text = re.sub("https:", "\r\nhttps:", input_text)

# Escribe el texto modificado en el archivo de salida
with open(output_file_path, 'w') as file:
    file.write(output_text)

print("Proceso completado. La salida se ha guardado en:", output_file_path)
```
Básicamente, lo que hace el código es tomar el documento ".txt" donde están guardadas las ligas copiadas del Sloan y dar ese "shift + enter" que separa liga por liga, para que el ".txt" no las interprete como una única liga gigante. 

En la carpeta con los programas que utilizarás para la descarga, recorte y demás cosas acerca de los datos, vas a encontrar el programa "separador". Este programa lo que hace es que toma tu archivo ".txt" donde copiaste las ligas del SDSS y, utilizando Regular Expressión de Python, separa las ligas bajo ciertos comandos, de tal modo que te genera un nuevo ".txt" con las ligas separas. 

De esa manera, ya puedes utilizar el nuevo ".txt" con ligas separadas para hacer la solicitud en tu terminal para descargar los FITS. Esto lo puedes hacer tanto en Windows como en Linux. Mi recomendación es utilizar Ubuntu o cualquier distribución similar para trabajar, porque te ahorras ciertos pasos confusos y molestos que necesitas en Windows. Aunque si prefieres trabajar desde Windows también se puede, yo estuve un buen rato con el SO de Microsoft y en general pude trabajar bien.

## Descargar FITS

Tanto en Windows como en Linux o Mac, lo primero que tendrás que bajar es Python y un IDE (entorno de desarrollo) como VScode, Pycharm o Spyder. Podrías trabajar también con código escrito desde un bloc de notas, si te acomodas a ello. Mi recomendación es utilizar VScode o Pycharm, me parece que son los más amigables. 

Lo segundo que deberás tener para bajar los gatos es "wget". Según ChatGPT:

> `wget` es una herramienta de línea de comandos disponible en sistemas operativos basados en Unix y Linux, así como en Windows, que se utiliza para descargar archivos desde la web de forma automática y sin intervención del usuario. Su nombre proviene de "Web Get".
>
> Con `wget`, puedes descargar archivos desde servidores HTTP, HTTPS y FTP, y es capaz de seguir enlaces recursivamente para descargar archivos y páginas web enteras. Es especialmente útil para descargar archivos grandes, como distribuciones de Linux, paquetes de software, archivos de datos, etc.
>
> Algunas características de `wget` incluyen la capacidad de reanudar descargas interrumpidas, descargar en segundo plano, limitar la velocidad de descarga, y más. Es una herramienta muy versátil y potente que es ampliamente utilizada por administradores de sistemas, desarrolladores web y usuarios avanzados de computadoras.

Para nuestro caso, "wget" va a ser una herramienta para bajar los FITS de manera automatizada. En Linux ya viene preinstalado, en Windows deberás instalarlo y en Mac la verdad no sé. Asumiendo que ya tienes "wget", los pasos para descargar los FITS serán los siguientes:

* Tener tu ".txt" con las ligas separadas
* Abrir una terminal de Linux, Windows o Mac, en la carpeta donde tengas tu ".txt". En Ubuntu puedes hacerlo solo con abrir archivos, dar clic derecho en la carpeta que utilizaremos y seleccionar "Abrir en una terminal". Si tu ".txt" está en "Downloads", entonces debería tener una terminar similar a esta:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/78e09d4c-22af-4600-830c-edf413489253)

* En mi caso, estoy en la siguiente ubicación:

 ![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/14379d79-7a48-4326-9789-b80e5de89948)
  
* Ahora, debemos utilizar "wget" tecleando en la terminal: "wget -i [nombre de tu archivo].txt":

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/946d34be-e848-4aeb-bbdf-53a77e05fc4c)


* Si lo hemos hecho bien, "wget" debería comenzar a trabajar y comenzará a descargar los FITS:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/62ffd8a8-315a-4d37-82ed-b4633514ef0b)


Una vez descargados los datos, podrás verlos comprimidos en la misma carpeta en la cual abriste tu terminal. Solo debes descomprimirlos para poder utilizarlos. Cuando tengas las versiones descomprimidas puedes borrar los archivos ".bz2" o ".zip", aunque no es necesario. Mi recomendación sería que no borres nada hasta que tengas tus datos al 100%. 

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/529d189a-d20a-4b23-b5bf-13c9b09c641e)

Descomprimido todo:

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/a3d0178c-9d0e-4189-b990-91541f055450)

Ahora ya tienes tus archivos FITS. Ya podemos pasar a la sección de recorte. Si quisieras acceder a los FITS directamente, necesitarías bajas un software como DS9 para poder visualizarlos, o utilizar Astropy en Python para poder plotearlos. De momento, confiaremos en que están bien. Después podemos entrar en detalles sobre DS9 y Astropy, que de hecho esa librería de Python la utilizaremos para el recorte de los FITS. 


## Recorte de los FITS

Anteriormente vimos que los FITS que el SDSS nos descarga son una fotografía grandota del cielo. Por ello necesitamos una manera de hacer los recortes para crear una especie de estampilla que nos de algo como lo siguiente:  

![image](https://github.com/CesarArcano97/Descarga-de-datos-SDSS/assets/66275063/e21d4d58-f704-4456-bbbc-84ba6d8cf74d)

Puedes encontrar la rutina bajo el nombre de 'Recorte-estampillas-SDSS.py' en los archivos del repositorio. El código es el siguiente:

```python
# Paqueterías

from astropy.nddata import Cutout2D
from astropy.wcs import WCS
import numpy as np  
import pandas as pd  # procesamiento de datos, lectura y escritura de archivos CSV (por ejemplo, pd.read_csv)
import glob
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from scipy import spatial
import os

'''
Es importante que las coordenadas vengan separadas en dos columnas y que no contengan otra cosa
'''

def main():
    coordenadas = r"/home/cesar/Documentos/Prueba-Felix-sloan-02-solo-coord.ods" #ruta del archivo con las coordenadas 
    imagenes = r"/home/cesar/Documentos/FITS-Felix/*.fits" #ruta de los archivos FITS 
    # el *.fits sirve para seleccionar todo archivo que termine en ".fits"
    out_path_fits = r"/home/cesar/Documentos/Recortes-prueba/FITS_recortadas" #ruta de salida para los recortes FITS
    out_path_ascii = r"/home/cesar/Documentos/Recortes-prueba/FITS_recortadas_ASCII" #ruta de salida para los recortes ASCII
    out_path_hdlv = r"/home/cesar/Documentos/Recortes-prueba/corrupt.txt" #corrupt.txt es importante.
    
    # En Windows, las rutas de archivos suelen ser de la siguiente manera:   
    # r"C:\Users\cesar\OneDrive\Documentos\Gelipses\Galaxias_elípticas.ods" 
    # en lugar de usar "/" utilizan el "\"
    # Por lo que si estás en Windows o Mac, habrá que cambiar las rutas de arriba

    df = pd.read_excel(coordenadas)
    fits_array = np.array(glob.glob(imagenes))
    plt.style.use(astropy_mpl_style)

    errores = open(out_path_hdlv, "w")

    for imagen_fits in fits_array:  # Itera sobre cada nombre de archivo FITS en la lista de archivos FITS
        hdu = fits.open(imagen_fits)[0]  # Abre el archivo FITS y obtiene el primer HDU (Header Data Unit)
        coord_fits = np.array((hdu.header['CRVAL1'], hdu.header['CRVAL2']))  # Obtiene las coordenadas RA y DEC del archivo FITS

        # Calcula las coordenadas relativas de los objetos en la imagen FITS
        coordinates = np.subtract(coord_fits, np.array(df[['ra', 'dec']]))  
        x = [(0, 0)]  # Punto de referencia para calcular la distancia euclidiana entre las coordenadas relativas
        distance, index = spatial.KDTree(coordinates).query(x)  # Utiliza un árbol KD para encontrar el índice del objeto más cercano en las coordenadas relativas

        t = np.array(df.iloc[index])  # Obtiene las coordenadas absolutas del objeto más cercano en la imagen FITS
        n, m = t[0][0], t[0][1]  # Separa las coordenadas RA y DEC del objeto más cercano

        recorte(n, m, imagen_fits, out_path_fits, out_path_ascii, errores)

    errores.close()

def recorte(ra, dec, file, out_path_fits, out_path_ascii, errores):
    try:
        file_name = os.path.splitext(os.path.basename(file))[0]
        
        # Convertir radec del objetivo a xy
        # ra, dec = (348.90253017155, 1.27188625068302)
        # ra, dec = n, m #argumento
        # ra, dec = (50.572811, -7.090685)
        w = WCS(file)
        x, y = w.all_world2pix(ra, dec, 1)

        # Cargar la imagen y su WCS
        hdu = fits.open(file)[0]
        wcs = WCS(hdu.header)

        position = (x, y)
        xdim = 126  # píxeles o ~50 arcsec; escala de píxeles nativa: 0.396 arcsec/píxel
        ydim = 126  # píxeles o ~50 arcsec; escala de píxeles nativa: 0.396 arcsec/píxel
        size = (ydim, xdim)  # debería darse en este orden

        # Preparando el recorte
        cutout = Cutout2D(hdu.data, position=position, size=size, wcs=wcs)

        # Poner los datos de la imagen en un HDU de fits (Unidad de Datos de Encabezado)
        hdu.data = cutout.data

        # Actualizar el encabezado de fits del recorte
        hdu.header.update(cutout.wcs.to_header())

        # Escribir el recorte en un nuevo archivo fits
        cutout_filename = os.path.join(out_path_fits, file_name + '_recorte' + '.fits') # i del loop
        hdu.writeto(cutout_filename, overwrite=True, checksum=True)

        # Cargar el recorte y su WCS
        hdulist = fits.open(cutout_filename)
        wcut = WCS(cutout_filename)

        # Cargar los datos científicos del recorte
        tbdata = hdulist[0].data

        # Escribir las coordenadas de los píxeles (físicos y mundiales) y los valores nativos en una tabla ASCII
        outfile = os.path.join(out_path_ascii, file_name + '.ascii')
        f = open(outfile, 'w')
        f.write("%s\n" % '#x_pix y_pix ra_deg dec_deg native_pixel_value')
        for i in range(ydim):
            for j in range(xdim):
                rac, decc = wcut.all_pix2world(j + 1, i + 1, 1)
                f.write("%s %s %s %s %s\n" % (j + 1, i + 1, rac, decc, tbdata[i, j]))

        f.close()
    except:
        print(file_name)
        errores.write(file_name + os.linesep)

if __name__=="__main__":
    main()
```

**Nota**: Recuerda cargas las paqueterías para poder procesar los datos. 

El código de recorte original fue realizado por Ángel Bongiovanni, investigador del _Institut de Radioastronomie Milimétrique_. Es conocido de José Antonio, por lo que seguramente te pedirá que lo cites en tu trabajo. El código de Bongiovanni solo servía para recortar una imagen por vez, así que me encargué de automatizarlo para que hiciera los recortes de todo el conjunto de FITS que le metas. Así que es una mezcla entre lo de Bongiovanni y lo que yo realicé para su automatización. 

Algunas cosas clave para utilizar el código:

* En la ruta de coordenadas debes tener una hoja de cálculo que solo contenga las coordenadas de tus objetos.
* En las rutas de los "out_path_fits", "out_path_ASCII" y "out_path_hdlv" debes asegurarte de que existan las carpetas en las que quieres que los recortes y muestras ASCII se alojen una vez realizado el proceso. Es decir, no puedes poner una ruta a una carpeta que no existe de antemano. 
* "out_path_fits": te devuelve los recortes de los FITS en la carpeta indicada. Son estampillas de 126x126 píxeles. 
* "out_path_ASCII": te devuelve los ASCII de los FITS en la carpeta indicada. Por si te sirve.
* Los "out_path_hdlv" te devuelven un ".txt" con archivos FITS corruptos, es decir, que por alguna razón no se pueden leer. 
* No te olvides de utilizar el "*.fits".

Básicamente, el proceso de automatización implica el uso de las coordenadas centrales de cada archivo FITS, alojada en el "Header" del FITS (básicamente los headers son tablas de datos que te dicen dónde se tomó la foto, a qué hora, altura, clima, coordenada central etc. etc.). Tenemos un conjunto de todas las coordenadas de nuestros objetos, así como la coordenada central de cada archivo FITS. Así, el programa compara cada imagen y selecciona el objeto cuyas coordenadas están más cercanas a las coordenadas centrales de esa imagen. Luego, crea un recorte de 126 × 126 píxeles que contiene al objeto.

Hemos hablado mucho sobre los FITS, así que sería buena idea que, si no lo estás ya, busques familiarizarte con estos archivos. Te dejo aquí un par de enlaces: 

* ¿Qué es el "Header" de un FITS? - [FITS Headers](https://docs.astropy.org/en/stable/io/fits/usage/headers.html).

* ¿Qué es un FITS file? - [A Primer on the FITS Data Format](https://fits.gsfc.nasa.gov/fits_primer.html).
* ¿Cómo manejar un FITS en python? - [Astropy | FITS File Handling](https://docs.astropy.org/en/stable/io/fits/).
* Más sobre los FITS - [Flexible Image Transport System (FITS)](https://www.loc.gov/preservation/digital/formats/fdd/fdd000317.shtml).



### Convertir los FITS en arrays

Probablemente ya conozcas numpy, una de las librerías más populares de Python. ChatGPT da las siguientes notas:



> NumPy es una biblioteca de Python ampliamente utilizada para computación numérica. Proporciona un conjunto de funciones y herramientas para trabajar con matrices y arreglos multidimensionales, lo que la hace especialmente útil para el análisis de datos, la computación científica y la manipulación de datos.
>
> Algunas de las características principales de NumPy son:
>
> 1. **Matrices y arreglos multidimensionales**: NumPy proporciona la clase `ndarray`, que es una estructura de datos eficiente para representar y manipular matrices y arreglos multidimensionales de manera homogénea.
> 2. **Funciones matemáticas**: NumPy incluye una amplia gama de funciones matemáticas para realizar operaciones numéricas en matrices y arreglos, como operaciones aritméticas, funciones trigonométricas, funciones exponenciales, funciones de álgebra lineal, etc.
> 3. **Indexación y segmentación avanzadas**: NumPy ofrece capacidades avanzadas de indexación y segmentación para acceder y manipular elementos individuales o subconjuntos de matrices y arreglos.
> 4. **Integración con otras bibliotecas**: NumPy se integra bien con otras bibliotecas de Python, como SciPy (para computación científica), Matplotlib (para visualización de datos), Pandas (para análisis de datos) y muchas más, lo que lo convierte en una parte integral del ecosistema de herramientas de análisis de datos en Python.



Podríamos decir que numpy sirve para crear, manipular y operar sobre vectores y matrices. Es importante que puedes convertir tus FITS en arreglos de numpy porque así conservas toda la información del arreglo (o matriz) que da forma a la imagen, pues si trabajaras con JPG o PNG perderías información. Digamos que lo más fiel al FITS es un arreglo numpy y como, de momento, los frameworks de redes neuronales no leen FITS, pues hay que trabajar con arrays. 

Puedes encontrar la rutina bajo el nombre de 'FITS-a-arrays-SDSS.py' en los archivos del repositorio. Para convertir tus FITS en numpy arrays, se diseñó este pequeño programa:

````python
import numpy as np 
import glob
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
import imageio
import os

def main():

    # Rutas de los archivos FITS de entrada y salida
    data_to_convert = r"/home/cesar/Documentos/Recortes-prueba/FITS_recortadas/*.fits"
    out_converted_data = r"/home/cesar/Documentos/Recortes-prueba/FITS_numpy"

    # Obtener una lista de archivos FITS en la carpeta de entrada
    fits_array = np.array(glob.glob(data_to_convert))
    plt.style.use(astropy_mpl_style)

    # Iterar sobre cada archivo FITS en la lista
    for imagen_fits in fits_array:
        # Abrir el archivo FITS para manipulación
        hdu = fits.open(imagen_fits)
        # Convertir el archivo FITS a un ndarray de numpy
        data = hdu[0].data  

        # Llamar a la función convertidor para guardar el archivo convertido
        convertidor(data, imagen_fits, out_converted_data)

def convertidor(data, file, out_converted_data):
    try:
        # Obtener el nombre base del archivo sin la extensión
        file_name = os.path.splitext(os.path.basename(file))[0]
        # Crear la ruta completa para el archivo convertido
        converted_filename = os.path.join(out_converted_data, file_name)
        # Guardar el archivo ndarray de numpy como un archivo .npy
        np.save(converted_filename, data)
        # Imprimir la ruta del archivo convertido
        print(converted_filename)

    except Exception as e:
        pass
        # Manejo de excepciones, en caso de que ocurra algún error durante la conversión
        #print(file_name)

if __name__=="__main__":
    main()

````



Las recomendaciones son las mismas que con el programa de recortes. En el fondo, trabajan de una manera muy similar. Con esto ya podrías comenzar a trabajar. 

### Notas adicionales

Puedes abrir y ver como quedaron tus recortes ya sea como un array o comu un FITS.

* Si quieres ver tu recorte como FITS, puedes utilizar astropy - [Read and plot an image from a FITS file](https://docs.astropy.org/en/stable/generated/examples/io/plot_fits-image.html).
* Si quieres ver tu recorte como array de numpy, puedes utilizar directamente Numpy o Matplotlib. 
* Recuerda que en todo entorno de Python (y de cualquier otro lenguaje) debes tener cargadas todas las paqueterías que vas a utilizar. 
* Revisar con calma cuando hay algún problema con la programación es esencial. Perder la paciencia solo nos entorpecerá aún más el camino. A veces es buena idea parar, despejarse un poco y volver después de un rato. 
