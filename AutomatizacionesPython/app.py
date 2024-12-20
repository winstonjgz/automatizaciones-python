import flet as ft
import sys
import os
from borrar_duplicados import find_duplicates, hash_file, delete_file, handle_folder_picker
from organizar_archivos import organize_folder
from redim_img import batch_resize
from convertidor_imagenes import convertir_imagen
from extraer_audio_de_videos import extract_audio



def main(page: ft.Page):
    page.title = "Automatizaciones con Python"
    page.window.width = 1000
    page.window.height = 750
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_800

    # Tema personalizado (debe ir antes de theme_mode)
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.TEAL,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.TEAL_700,
            secondary=ft.Colors.AMBER_500,
            background=ft.Colors.GREY_200,
            surface=ft.Colors.WHITE,
        )
    )

    # Definir el modo del tema
    page.theme_mode = ft.ThemeMode.DARK

    # Variables de estado
    state = {
        "current_duplicates": [],
        "current_view": "duplicates",
        "resize_input_folder": "",
        "resize_output_folder": "",
        "selecting_resize_output": False,
        "convert_input_file": "",
        "extract_audio_input_file": "",
        "audio_extraction_progress": 0,
        "total_videos":0,
        "current_videos": "",
    }

    selected_dir_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )

    result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    duplicates_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )

    delete_all_button = ft.ElevatedButton(
        text="Eliminar todos los duplicados",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_900,
        icon=ft.Icons.DELETE_SWEEP,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )


    #Controles de el organizador
    organize_dir_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )

    organize_success_text = ft.Text(
        size=14,
        weight=ft.FontWeight.BOLD,
    )

    convert_img_text = ft.Text(
        value="No se ha seleccionado ninguna imagen",
        size=14,
        color=ft.Colors.BLUE_200
    )

    convert_img_result_text = ft.Text(
        size=14,
        weight=ft.FontWeight.BOLD
    )

    extract_audio_text = ft.Text(
        value="No se ha seleccionado ningun video",
        size=14,
        color=ft.Colors.BLUE_200
    )

    extract_audio_result_text = ft.Text(
        size=14,
        weight=ft.FontWeight.BOLD
    )


    format_dropdown = ft.Dropdown(
        label="Formato de salida",
        width=200,
        options=[
            ft.dropdown.Option('PNG'),
            ft.dropdown.Option('JPEG'),
            ft.dropdown.Option('WEBP'),
            ft.dropdown.Option('BMP'),
            ft.dropdown.Option('GIF'),
        ],
        value='PNG'
    )

    #Controles extraccion de audio
    extract_audio_input_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )

    extract_audio_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)
    audio_progress = ft.ProgressBar(width=400, visible=False)
    current_video_text = ft.Text(size=14, color=ft.Colors.BLUE_200)


    def handle_file_picker(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) >0:
            file_path = e.files[0].path
            state["convert_input_file"] = file_path
            convert_img_text.value = f"Imagen seleccionada: {file_path}"
            convert_img_text.update()

    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            if state["current_view"] == "duplicates":
                selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
                selected_dir_text.update()
                scan_directory(e.path)
            elif state["current_view"] == "organize":
                organize_dir_text.value = f"Carpeta seleccionada: {e.path}"
                organize_dir_text.update()
                organize_directory(e.path)
            elif state["current_view"] == "resize":
                if state["selecting_resize_output"]:
                    state["resize_output_folder"] = e.path
                    resize_output_text.value = f"Carpeta de salida: {e.path}"
                    resize_output_text.update()
                else:
                    state["resize_input_folder"] = e.path
                    resize_input_text.value = f"Carpeta de entrada: {e.path}"
                    resize_input_text.update()
            elif state["current_view"] == "extract_audio":
                state["extract_audio_input_file"] = e.path
                extract_audio_input_text.value = f"Carpeta seleccionada: {e.path}"
                extract_audio_input_text.update()

    # Modulo para redimensionar imagenes
    def select_input_folder():
        state["selecting_resize_output"] = False
        folder_picker.get_directory_path()

    def select_output_folder():
        state["selecting_resize_output"] = True
        folder_picker.get_directory_path()

    def resize_images():
        try:
            if not state["resize_input_folder"] or not state["resize_output_folder"]:
                resize_result_text.value = "Error: Selecciona las carpetas de origen y destino"
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return
            width_new = int(width_field.value)
            height_new = int(height_field.value)

            if width_new<= 0 or height_new<=0:
                resize_result_text.value = "Error: Las dimensiones deben ser mayores a 0"
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return
            batch_resize(state["resize_input_folder"], state["resize_output_folder"], width_new, height_new)
            resize_result_text.value = "Imagenes redimensionadas exitosamente"
            resize_result_text.color = ft.Colors.GREEN_400
            resize_result_text.update()
        except ValueError:
            resize_result_text.value = "Error: Ingresa dimensiones validas"
            resize_result_text.color = ft.Colors.RED_400
            resize_result_text.update()
        except Exception as e:
            resize_result_text.value = f"Error: al redimensionar {str(e)}"
            resize_result_text.color = ft.Colors.RED_400
            resize_result_text.update()


    # Modulo para organizar directorios en carpetas

    def organize_directory(directory):
        try:
            organize_folder(directory)
            organize_success_text.value = "Archivos organizados exitosamente"
            organize_success_text.color = ft.Colors.GREEN_400
        except Exception as e:
            organize_success_text.value = f"Error al organizar archivos: {str(e)}"
            organize_success_text.color = ft.Colors.RED_400
        organize_success_text.update()

    def scan_directory(directory):
        duplicates_list.controls.clear()
        state["current_duplicates"] = find_duplicates(directory)

        if not state["current_duplicates"]:
            result_text.value = "No se encontraron archivos duplicados"
            result_text.color = ft.Colors.GREEN_400
            delete_all_button.visible = False
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados"
            result_text.color = ft.Colors.ORANGE_400
            delete_all_button.visible = True

            for dup_file, original in state['current_duplicates']:
                dup_row = ft.Row([
                    ft.Text(
                        value=f"Duplicado: {dup_file} \n Original: {original}",
                        size=12,
                        expand=True,
                        color=ft.Colors.BLUE_200,
                    ),
                    ft.ElevatedButton(
                        text="Eliminar",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_900,
                        on_click=lambda e, path=dup_file: delete_duplicate(path)
                    )
                ]
                )
                duplicates_list.controls.append(dup_row)
        duplicates_list.update()
        delete_all_button.update()
        result_text.update()


    #Modulo para borrar archivos duplicados

    def delete_all_duplicates():
        deleted_count = 0
        failed_count = 0

        for dup_file, _ in state["current_duplicates"]:
            if delete_file(dup_file):
                deleted_count += 1
            else:
                failed_count += 1

        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Se eliminaron exitosamente {deleted_count} archivos!"
            result_text.color = ft.Colors.GREEN_400
        else:
            result_text.value = f"Se eliminaron exitosamente {deleted_count} archivos. Fallaron {failed_count} archivos a ser borrados!"
            result_text.color = ft.Colors.RED_400

        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Se elimino exitosamente: {filepath} !"
            result_text.color = ft.Colors.GREEN_400
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
            state["current_duplicates"] = [(dup, orig) for dup, orig in state["current_duplicates"] if dup != filepath]
            if not state["current_duplicates"]:
                delete_all_button.visible = False
        else:
            result_text.value = f"No se elimino: {filepath} !"
            result_text.color = ft.Colors.RED_400

        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    # Configurar selector de archivos
    file_picker = ft.FilePicker(
        on_result=handle_file_picker
    )
    file_picker.file_type = ft.FilePickerFileType.IMAGE
    file_picker.allowed_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']

    # Configurar el selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.extend([folder_picker, file_picker])



    def resource_path(relative_path):
        """Obtiene la ruta absoluta del recurso, funciona para .exe o ejecución directa"""
        try:
            base_path = sys._MEIPASS  # Directorio temporal donde PyInstaller coloca archivos
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    image_path = resource_path("assets/automatizacion4.png")

    #Corvertir imagen
    def convertir_imagen_fin():
        try:
            if not state["convert_input_file"]:
                convert_img_result_text.value = "Error: Selecciona una imagen"
                convert_img_result_text.color = ft.Colors.RED_400
                convert_img_result_text.update()
                return
            if not format_dropdown.value:
                convert_img_result_text.value = "Error: Selecciona un formato de salida"
                convert_img_result_text.color = ft.Colors.RED_400
                convert_img_result_text.update()
                return
            convertir_imagen(state["convert_input_file"], format_dropdown.value)
            convert_img_result_text.value = "Imagen convertida exitosamente"
            convert_img_result_text.color = ft.Colors.GREEN_400
            convert_img_result_text.update()
        except Exception as e:
            convert_img_result_text.value = f"Error al convertir imagen: {str(e)}"
            convert_img_result_text.color = ft.Colors.RED_400
            convert_img_result_text.update()

    def extraer_audio():
        try:
            if not state["extract_audio_input_file"]:
                extract_audio_result_text.value= "Error: Selecciona una carpeta con videos"
                extract_audio_result_text.color= ft.Colors.RED_400
                extract_audio_result_text.update()
                return

            input_folder = state["extract_audio_input_file"]
            output_folder = os.path.join(input_folder, "audios")
            os.makedirs(output_folder, exist_ok=True)

            audio_progress.value=0
            audio_progress.visible = True
            audio_progress.update()

            def progress_callback(current, total, archivo):
                progress = current / total
                audio_progress.value = progress
                audio_progress.update()
                current_video_text.value = f"Procesando {archivo}: {current}/{total}"
                current_video_text.update()

            extract_audio(input_folder, output_folder, progress_callback)

            extract_audio_result_text.value= "Extraccion completada. Los archivos de audio se guardaron en la carpeta 'audios'"
            extract_audio_result_text.color= ft.Colors.GREEN_400
            current_video_text.value= "Proceso finalizado!!"

        except Exception as e:
            extract_audio_result_text.value= f"Error durante la extraccion: {str(e)}"
            extract_audio_result_text.color= ft.Colors.RED_400

        finally:
            audio_progress.visible = False
            audio_progress.update()

        extract_audio_result_text.update()
        current_video_text.update()


    # Vista de inicio
    home_view = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        value="¡Bienvenido al Sistema de Automatizaciones!",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.TEAL_300,
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Container(
                    content=ft.Text(
                        value="Explora las herramientas y simplifica tus tareas.",
                        size=20,
                        weight=ft.FontWeight.NORMAL,
                        color=ft.Colors.GREY_400,
                    ),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Container(
                    content=ft.Image(
                        src=image_path,
                        width=500,
                        height=400,
                        fit=ft.ImageFit.COVER,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),# Ajusta la imagen para cubrir el contenedor
                    ),

                    alignment=ft.alignment.center,  # Centra el contenido
                ),
                ft.Container(
                    content=ft.Text(
                        value="Automatizaciones creadas con Python y Flet.",
                        size=14,
                        weight=ft.FontWeight.NORMAL,
                        color=ft.Colors.GREY_400,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=30,
        expand=True,
    )

    # Vista de archivos duplicados
    duplicate_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Eliminar archivos duplicados",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Seleccionar carpeta",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: folder_picker.get_directory_path()
                ),
                delete_all_button,
            ]),
            ft.Container(
                content=selected_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            result_text,

            ft.Container(
                content=duplicates_list,
                border=ft.border.all(width=2, color=ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
                expand=True,
            )
        ]),
        padding=30,
        expand=True,
    )

    # Vista de archivos a organizar
    organize_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Organizar archivos por tipo",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Seleccionar carpeta",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: folder_picker.get_directory_path()
                ),

            ]),
            ft.Container(
                content=organize_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            organize_success_text,

            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Los archivos seran organizados en las siguientes carpetas: ",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(value="• Imagenes': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp', '.tif', '.ico', '.odg']", size=14),
                    ft.Text(value="• Videos': ['.mp4', '.mkv', '.avi', '.mov', '.mpg', '.3gp', '.wmv', '.dvd', '.ogg', '.flv']", size=14),
                    ft.Text(value="• Documentos PDF': ['.pdf']", size=14),
                    ft.Text(value="• Documentos Word': ['.doc', '.txt', '.docx', '.odt']", size=14),
                    ft.Text(value="• Documentos Excel-Calc': ['.xls', '.xlsx', '.xlsm', '.ods']", size=14),
                    ft.Text(value="• Presentaciones': ['.ppt', '.pptx', '.odp']", size=14),
                    ft.Text(value="• Datasets': ['.csv', '.mdb', '.sav', '.accdb', '.sql']", size=14),
                    ft.Text(value="• Programas': ['.exe', '.msi']", size=14),
                    ft.Text(value="• Comprimidos': ['.rar', '.zip', '.tgz']", size=14),
                    ft.Text(value="• Imagenes Sistemas': ['.iso', '.deb']", size=14),
                    ft.Text(value="• Audios': ['.mp3']", size=14),
                ]),
                border=ft.border.all(width=2, color=ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True,
    )

    # Controles vista redimensionar imagenes
    resize_input_text = ft.Text(
        value="Carpeta de entrada: No seleccionada",
        size=14,
        color= ft.Colors.BLUE_200
    )

    resize_output_text = ft.Text(
        value="Carpeta de salida: No seleccionada",
        size=14,
        color=ft.Colors.BLUE_200
    )

    resize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    width_field = ft.TextField(
        label= "Ancho",
        value="800",
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,

    )

    height_field = ft.TextField(
        label="Alto",
        value="600",
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,

    )



    # Vista redimensionar imagenes
    resize_img_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Redimensionar",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Seleccionar carpeta de entrada",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: select_input_folder()
                ),
                ft.ElevatedButton(
                    text="Seleccionar carpeta de salida",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: select_output_folder()
                ),
            ]),
            ft.Container(
                content=ft.Column([
                    resize_input_text,
                    resize_output_text
                ]),
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Dimensiones imagen",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Row([
                        width_field,
                        ft.Text(value='x', size=20),
                        height_field,
                        ft.Text(value="pixeles", size=14)
                    ]),
                ]),
                margin=ft.margin.only(bottom=10)
            ),
            ft.ElevatedButton(
                text="Redimensionar Imagenes",
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                color= ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: resize_images()
            ),
            resize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información: ",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(
                        value="• Se procesaran archivos de tipo: .jpg, .jpeg y .png",
                        size=14),
                    ft.Text(
                        value="• Las imagenes originales no seran modificadas",
                        size=14),
                    ft.Text(value="• Las imagenes redimensionadas se guardaran con el prefijo 'resized'", size=14),

                ]),
                border=ft.border.all(width=2, color=ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True

    )

    # Vista convertir imagenes
    convert_img_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Convertir formato de imagen",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),

            ft.ElevatedButton(
                text="Seleccionar imagen",
                icon=ft.Icons.IMAGE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: file_picker.pick_files()
            ),
            ft.Container(
                content=ft.Column([
                    convert_img_text,
                ]),

                margin=ft.margin.only(top=10, bottom=10)
            ),
            format_dropdown,


            ft.ElevatedButton(
                text="Convertir Imagen",
                icon=ft.Icons.TRANSFORM,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: convertir_imagen_fin()
            ),
            convert_img_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información: ",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(
                        value="• Formatos soportados: .webp, .bmp, .gif, .jpeg y .png",
                        size=14),
                    ft.Text(
                        value="• La imagen original no sera modificada",
                        size=14),
                    ft.Text(
                        value="• La imagen convertida se guardara en la misma carpeta",
                        size=14),
                    ft.Text(value="• Al convertir en JPEG las imagenes con tranaparencia se convertiran a fondo blanco", size=14),

                ]),
                border=ft.border.all(width=2, color=ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True

    )

    # Vista extraer audios
    extract_audio_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Extraer audio de videos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),

            ft.ElevatedButton(
                text="Seleccionar carpeta de videos",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: ""
            ),
            ft.Container(
                content=ft.Column([
                    extract_audio_text,
                ]),

                margin=ft.margin.only(top=10, bottom=10)
            ),

            ft.ElevatedButton(
                text="Extraer audio",
                icon=ft.Icons.AUDIOTRACK,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: ''
            ),
            extract_audio_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información: ",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(
                        value="• Formatos de videos soportados: .mp4, .avi, .mov, y .mkv",
                        size=14),
                    ft.Text(
                        value="• Los archivos de audio se extraeran en formato .mp3",
                        size=14),
                    ft.Text(
                        value="• Los audios extraidos se guardaran en una carpeta 'audios' dentro de la carpeta seleccionada",
                        size=14),
                    ft.Text(value="• Los archivos de video originales no seran modificados",
                            size=14),

                ]),
                border=ft.border.all(width=2, color=ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True

    )

    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            state["current_view"] = "home"
            content_area.content = home_view
        elif selected ==1:
            state["current_view"] = "duplicates"
            content_area.content = duplicate_files_view
        elif selected == 2:
            state["current_view"] = "organize"
            content_area.content = organize_files_view
        elif selected == 3:
            state["current_view"] = "resize"
            content_area.content = resize_img_view
        elif selected == 4:
            state["current_view"] = "convert_img"
            content_area.content = convert_img_view
        elif selected == 5:
            state["current_view"] = "extract_audio"
            content_area.content = extract_audio_view
        elif selected == 6:
            state["current_view"] = "develop"
            content_area.content = ft.Text(value="Próximo desarrollo", size=24)
        content_area.update()

    content_area = ft.Container(
        content=home_view,
        margin=ft.margin.only(bottom=10),
        expand=True,
    )

    # Menu lateral

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME,
                selected_icon=ft.Icons.HOME,
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE_FOREVER,
                selected_icon=ft.Icons.DELETE_FOREVER,
                label="Duplicados"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                selected_icon=ft.Icons.FOLDER_COPY,
                label="Organizar"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                selected_icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                label="Redimensionar"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CAMERA_ALT_OUTLINED,
                selected_icon=ft.Icons.CAMERA_ALT_OUTLINED,
                label="Convertir"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.AUDIOTRACK,
                selected_icon=ft.Icons.AUDIOTRACK,
                label="Extraer Audio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD_HOME_WORK,
                selected_icon=ft.Icons.ADD_HOME_WORK,
                label="En desarrollo"
            )

        ],
        on_change=change_view,
        bgcolor=ft.Colors.GREY_900,
    )


    # Footer con información de la versión y el año
    footer = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    value="© 2024 Winston Guzmán",
                    size=12,
                    color=ft.Colors.GREY_600,
                ),
                ft.Text(
                    value="v1.0.0",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.RIGHT,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.all(10),
        bgcolor=ft.Colors.GREY_100,
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_300)),

    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        rail,
                        ft.VerticalDivider(width=1),
                        content_area,
                    ],
                    expand=True,
                ),
                footer,
            ],
            spacing=0,
            expand=True,
        )
    )



if __name__ == "__main__":
    ft.app(target=main)
