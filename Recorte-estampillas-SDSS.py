from astropy.nddata import Cutout2D  # Importar Cutout2D para recortar imágenes
from astropy.wcs import WCS  # Importar WCS para trabajar con sistemas de coordenadas
import numpy as np  # Importar numpy para manipulación de arrays
import pandas as pd  # Importar pandas para procesamiento de datos
import glob  # Importar glob para búsqueda de archivos
import matplotlib.pyplot as plt  # Importar matplotlib para graficar
from astropy.visualization import astropy_mpl_style  # Importar estilo de Astropy para gráficos
from astropy.utils.data import get_pkg_data_filename  # Importar función para obtener nombre de archivos de Astropy
from astropy.io import fits  # Importar fits de Astropy para trabajar con archivos FITS
from scipy import spatial  # Importar spatial de scipy para operaciones espaciales
import os  # Importar os para manipulación de archivos del sistema

'''
Es importante que las coordenadas vengan separadas en dos columnas y que no contengan otra cosa
'''

def main():
    # Ruta del archivo con las coordenadas
    coordenadas = r"/home/cesar/Documentos/Prueba-Felix-sloan-02-solo-coord.ods"
    # Ruta de los archivos FITS
    imagenes = r"/home/cesar/Documentos/FITS-Felix/*.fits"
    # Ruta de salida para los recortes FITS
    out_path_fits = r"/home/cesar/Documentos/Recortes-prueba/FITS_recortadas"
    # Ruta de salida para los recortes ASCII
    out_path_ascii = r"/home/cesar/Documentos/Recortes-prueba/FITS_recortadas_ASCII"
    # Ruta para el archivo de errores
    out_path_hdlv = r"/home/cesar/Documentos/Recortes-prueba/corrupt.txt"

    '''
    En Windows, las rutas de archivos suelen ser de la siguiente manera:   
    r"C:\Users\cesar\OneDrive\Documentos\Gelipses\Galaxias_elípticas.ods" 
    # en lugar de usar "/" utilizan el "\"
    Por lo que si estás en Windows o Mac, habrá que cambiar las rutas de arriba
    '''

    # Leer el archivo de coordenadas
    df = pd.read_excel(coordenadas)
    # Obtener una lista de archivos FITS en la ruta especificada
    fits_array = np.array(glob.glob(imagenes))
    # Establecer el estilo de gráfico
    plt.style.use(astropy_mpl_style)

    # Abrir el archivo de errores en modo escritura
    errores = open(out_path_hdlv, "w")

    # Iterar sobre cada archivo FITS en la lista
    for imagen_fits in fits_array:
        # Abrir el archivo FITS y obtener las coordenadas del header
        hdu = fits.open(imagen_fits)[0]
        coord_fits = np.array((hdu.header['CRVAL1'], hdu.header['CRVAL2']))

        # Calcular las diferencias entre las coordenadas FITS y las coordenadas del DataFrame
        coordinates = np.subtract(coord_fits, np.array(df[['ra', 'dec']]))
        x = [(0, 0)]
        # Encontrar la distancia mínima entre las coordenadas FITS y las coordenadas del DataFrame
        distance, index = spatial.KDTree(coordinates).query(x)

        # Obtener las coordenadas más cercanas en el DataFrame
        t = np.array(df.iloc[index])
        n, m = t[0][0], t[0][1]

        # Realizar el recorte y escribir los archivos de salida
        recorte(n, m, imagen_fits, out_path_fits, out_path_ascii, errores)

    # Cerrar el archivo de errores
    errores.close()

def recorte(ra, dec, file, out_path_fits, out_path_ascii, errores):
    try:
        # Obtener el nombre base del archivo FITS
        file_name = os.path.splitext(os.path.basename(file))[0]
        
        # Convertir ra y dec del objetivo a coordenadas de píxeles
        w = WCS(file)
        x, y = w.all_world2pix(ra, dec, 1)

        # Cargar la imagen FITS y su WCS
        hdu = fits.open(file)[0]
        wcs = WCS(hdu.header)

        position = (x, y)
        xdim = 126  # Número de píxeles en la dimensión x
        ydim = 126  # Número de píxeles en la dimensión y
        size = (ydim, xdim)  # Tamaño del recorte

        # Realizar el recorte
        cutout = Cutout2D(hdu.data, position=position, size=size, wcs=wcs)

        # Actualizar el header FITS con el WCS del recorte
        hdu.data = cutout.data
        hdu.header.update(cutout.wcs.to_header())

        # Escribir el recorte en un nuevo archivo FITS
        cutout_filename = os.path.join(out_path_fits, file_name + '_recorte' + '.fits')
        hdu.writeto(cutout_filename, overwrite=True, checksum=True)

        # Cargar el recorte y su WCS
        hdulist = fits.open(cutout_filename)
        wcut = WCS(cutout_filename)

        # Obtener los datos científicos del recorte
        tbdata = hdulist[0].data

        # Escribir las coordenadas de los píxeles y los valores de los píxeles en un archivo ASCII
        outfile = os.path.join(out_path_ascii, file_name + '.ascii')
        f = open(outfile, 'w')
        f.write("%s\n" % '#x_pix y_pix ra_deg dec_deg native_pixel_value')
        for i in range(ydim):
            for j in range(xdim):
                rac, decc = wcut.all_pix2world(j + 1, i + 1, 1)
                f.write("%s %s %s %s %s\n" % (j + 1, i + 1, rac, decc, tbdata[i, j]))

        f.close()
    except Exception as e:
        print(file_name)
        # Escribir el nombre del archivo en el archivo de errores
        errores.write(file_name + os.linesep)

if __name__ == "__main__":
    # Ejecutar la función principal si el script es ejecutado directamente
    main()

