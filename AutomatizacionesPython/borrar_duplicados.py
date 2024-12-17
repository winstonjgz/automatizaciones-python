import os
import hashlib
import flet as ft


def hash_file(filename):
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder):
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            fullpath = os.path.join(dirpath, f)
            file_hash = hash_file(fullpath)
            if file_hash in hashes:
                duplicates.append((fullpath, hashes[file_hash]))
            else:
                hashes[file_hash] = fullpath
    return duplicates


def delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        return False


def handle_folder_picker(e: ft.FilePickerResultEvent):
    if e.path:
        selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
        selected_dir_text.update()
