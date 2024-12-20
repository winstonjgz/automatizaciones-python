# Automatizaciones de Carpetas y Archivos

Este proyecto es una aplicación para automatizar tareas relacionadas con la organización de archivos y la eliminación de archivos duplicados en directorios. Fue desarrollado con Python y la biblioteca [Flet](https://flet.dev/) para proporcionar una interfaz gráfica de usuario amigable y moderna.

## Características

1. **Eliminación de Archivos Duplicados**:
   - Escanea una carpeta seleccionada para encontrar archivos duplicados basados en su hash.
   - Permite eliminar archivos duplicados individualmente o en masa.

2. **Organización de Archivos**:
   - Organiza los archivos en carpetas según su tipo. 
   - Los archivos se distribuyen en carpetas como `Imagenes`, `Videos`, `Documentos`, `Presentaciones`, etc.

3. **Interfaz Gráfica**:
   - Diseño intuitivo y adaptado al modo oscuro.
   - Opciones claras para seleccionar carpetas y realizar acciones.

## Cómo Funciona
### Eliminación de Archivos Duplicados
Selecciona la pestaña "Duplicados" en el menú lateral.
Haz clic en "Seleccionar carpeta" para elegir el directorio a escanear.
La aplicación mostrará una lista de archivos duplicados encontrados:
Puedes eliminar archivos específicos.
También puedes eliminarlos todos con un solo clic.

### Organización de Archivos
Selecciona la pestaña "Organizar" en el menú lateral.
Haz clic en "Seleccionar carpeta" para elegir el directorio a organizar.
Los archivos se moverán automáticamente a carpetas correspondientes según su tipo.

#### Tipos de Archivos Soportados
- Imágenes: `.jpeg`, `.jpg`, `.png`, `.gif`, `.bmp`, `.webp`
- Videos: `.mp4`, `.mkv`, `.avi`, `.mov`
- Documentos: `.pdf`, `.doc`, `.txt`, `.docx`, `.xls`, `.xlsx`, `ppt`, etc.
- Otros: Archivos comprimidos, programas, datasets, entre otros.

Capturas de Pantalla
(Aquí puedes agregar imágenes o gifs mostrando la interfaz de tu aplicación)

### Redimensionador de Imagenes
Selecciona la pestaña "Redimensionar" en el menu general.
Haz clic en "Seleccionar carpeta de entrada" para elegir el directorio donde estan las imagenes.
Haz clic en "Seleccionar carpeta de salida" para elegir el directorio donde van las imagenes redimensionadas.
Coloca en numero el alto y ancho deseado.
Haz clic en "Redimensionar Imagenes" para ejecutar el redimensionado.


## Instalacion de dependencias
pip install -r requirements.txt

Adaptado por 💻 por Winston Guzmán de los videos de Codigo Espinoza en Youtube.

