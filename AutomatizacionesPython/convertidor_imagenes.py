import os
from PIL import Image

def convertir_imagen(ruta_entrada, formato_salida):
    try:
        nombre_base = os.path.splitext(ruta_entrada)[0]

        with Image.open(ruta_entrada) as img:
            # Si la imagen esta en modo RGBA y convertimos a JPEG convertir a RGB
            if img.mode in ('RGBA', 'LA') and formato_salida.upper() == 'JPEG':
                img = img.convert('RGB')

            #Crear nombre salida
            ruta_salida = f"{nombre_base}.{formato_salida.lower()}"

            #Guardar imagen
            img.save(ruta_salida, formato_salida.upper())
            print(f"Imagen convertida exitosamente: {ruta_salida}")

    except Exception as e:
        print(f"Error al convertir la imagen: {str(e)}")
