import flet as ft
from borrar_duplicados import find_duplicates, hash_file, delete_file

def main(page: ft.Page):
    page.title = "Borrado de archivos duplicados"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_800
    page.theme_mode = ft.ThemeMode.DARK

    # Tema personalizado
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme = ft.ColorScheme(
            primary=ft.Colors.BLUE,
            secondary=ft.Colors.ORANGE,
            background= ft.Colors.GREY_900,
            surface=ft.Colors.GREY_800,
        )
    )

    #Variables de estado
    state = {
        "current_duplicates" : [],
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
        color= ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_900,
        icon=ft.Icons.DELETE_SWEEP,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )


    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
            selected_dir_text.update()
            scan_directory(e.path)

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
                        on_click=lambda e, path = dup_file: delete_duplicate(path)
                    )
                    ]
                )
                duplicates_list.controls.append(dup_row)
        duplicates_list.update()
        delete_all_button.update()
        result_text.update()

    def delete_all_duplicates():
        deleted_count = 0
        failed_count = 0

        for dup_file, _ in state["current_duplicates"]:
            if delete_file(dup_file):
                deleted_count +=1
            else:
                failed_count +=1

        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Se eliminaron exitosamente {deleted_count} archivos!"
            result_text.color= ft.Colors.GREEN_400
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


    #Configurar el selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)

    #Vista de archivos duplicados
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
                    text="Seleccionar carperta",
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


    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            #content_area.content = ft.Text(value= "Vista de Duplicados", size = 24)
            content_area.content = duplicate_files_view
        elif selected == 1:
            content_area.content = ft.Text(value= "En desarrollo", size = 24)
        content_area.update()

    content_area = ft.Container(
        #content=ft.Text(value="Vista de Duplicados", size=24),
        content= duplicate_files_view,
        expand=True,

    )

    #Menu lateral

    rail = ft.NavigationRail(
        selected_index=0,
        label_type= ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE_FOREVER,
                selected_icon=ft.Icons.DELETE_FOREVER,
                label="Duplicados"
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



    """page.add(
    ft.Container(
        content= ft.Column(
            controls= [
                ft.Text(
                    value="Eliminar archivos duplicados",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                    ),
                ft.ElevatedButton(
                    text="Boton de ejemplo",
                    icon=ft.Icons.PLAY_ARROW
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
        )
    )"""

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area
            ],
            expand=True,

        )
    )




if __name__ == "__main__":
    ft.app(target=main)