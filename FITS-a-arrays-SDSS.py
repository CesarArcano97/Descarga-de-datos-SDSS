import numpy as np  # Importar numpy para manipulación de arrays
import glob  # Importar glob para búsqueda de archivos
import matplotlib.pyplot as plt  # Importar matplotlib para graficar
from astropy.visualization import astropy_mpl_style  # Importar estilo de Astropy para gráficos
from astropy.io import fits  # Importar fits de Astropy para trabajar con archivos FITS
import imageio  # Importar imageio para manipulación de imágenes
import os  # Importar os para manipulación de archivos del sistema

def main():
    # Ruta de los archivos FITS a convertir
    data_to_convert = r"/home/usuario/Documentos/Recortes-prueba/FITS_recortadas/*.fits"
    # Ruta de salida para los archivos convertidos
    out_converted_data = r"/home/usuario/Documentos/Recortes-prueba/FITS_numpy"

    # Obtener una lista de archivos FITS en la ruta especificada
    fits_array = np.array(glob.glob(data_to_convert))
    # Establecer el estilo de gráfico
    plt.style.use(astropy_mpl_style)

    # Iterar sobre cada archivo FITS en la lista
    for imagen_fits in fits_array:
        # Abrir el archivo FITS
        hdu = fits.open(imagen_fits)
        # Convertir el archivo FITS a un ndarray de numpy
        data = hdu[0].data  

        # Llamar a la función convertidor para convertir el archivo
        convertidor(data, imagen_fits, out_converted_data)

def convertidor(data, file, out_converted_data):
    try:
        # Extraer el nombre base del archivo FITS
        file_name = os.path.splitext(os.path.basename(file))[0]
        # Crear el nombre de archivo convertido
        converted_filename = os.path.join(out_converted_data, file_name)
        # Guardar el ndarray como archivo .npy
        np.save(converted_filename, data)
        # Imprimir la ruta del archivo convertido
        print(converted_filename)

    except Exception as e:
        pass
        # Manejar excepciones en caso de error

if __name__ == "__main__":
    # Ejecutar la función principal si el script es ejecutado directamente
    main()

