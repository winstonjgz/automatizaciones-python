import os
import shutil


def organize_folder(folder):
    file_types = {
        'Imagenes': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp', '.tif', '.ico', '.odg'],
        'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.mpg', '.3gp', '.wmv', '.dvd', '.ogg', '.flv'],
        'Documentos PDF': ['.pdf'],
        'Documentos Word': ['.doc', '.txt', '.docx', '.odt'],
        'Documentos Excel-Calc': ['.xls', '.xlsx', '.xlsm', '.ods'],
        'Presentaciones': ['.ppt', '.pptx', '.odp'],
        'Datasets': ['.csv', '.mdb', '.sav', '.accdb', '.sql'],
        'Programas': ['.exe', '.msi'],
        'Comprimidos': ['.rar', '.zip', '.tgz'],
        'Imagenes Sistemas': ['.iso', '.deb'],
        'Audios': ['.mp3']

    }
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f'Archivo {filename} movido a {folder_name}')
