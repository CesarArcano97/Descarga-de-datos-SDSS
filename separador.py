import re  # Importar el módulo de expresiones regulares

# Ruta del archivo de entrada y salida
input_file_path = r"/home/cesar/Documentos/Recortes-prueba/datos-sdss-ligas.txt"
output_file_path = r"/home/cesar/Documentos/Recortes-prueba/ligas-separadas.txt"  # Reemplaza "/ruta/a/la/carpeta/salida/salida.txt" con la ruta de la carpeta de salida deseada y el nombre del archivo de salida

# Leer el contenido del archivo de entrada
with open(input_file_path, 'r') as file:
    input_text = file.read()

# Realizar la sustitución en el texto leído
output_text = re.sub("https:", "\r\nhttps:", input_text)

# Escribir el texto modificado en el archivo de salida
with open(output_file_path, 'w') as file:
    file.write(output_text)

print("Proceso completado. La salida se ha guardado en:", output_file_path)
