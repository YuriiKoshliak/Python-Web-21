import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import logging

# Налаштування журналу
logging.basicConfig(filename='sort_files.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8')

def move_file(file_path, dest_folder, file_extension):
    extension_folder = os.path.join(dest_folder, file_extension)
    if not os.path.exists(extension_folder):
        os.makedirs(extension_folder)
    try:
        shutil.move(file_path, extension_folder)
        logging.info(f"Файл {file_path} переміщено до {extension_folder}")
    except Exception as e:
        logging.error(f"Помилка при переміщенні файлу {file_path}: {e}")

def sort_files(folder_path, dest_folder):
    if not os.path.exists(folder_path):
        logging.error(f"Папка {folder_path} не існує.")
        return

    # Створення пулу потоків
    with ThreadPoolExecutor(max_workers=5) as executor:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                # Отримання розширення файлу
                file_extension = item.split('.')[-1] if '.' in item else 'unknown'
                # Переміщення файлу в нову папку
                executor.submit(move_file, item_path, dest_folder, file_extension)
            elif os.path.isdir(item_path):
                # Рекурсивний виклик функції для підкаталогів
                executor.submit(sort_files, item_path, dest_folder)

# Шлях до папки, яку потрібно сортувати
folder_path = 'unsorted_folder'
# Шлях до папки, де будуть створюватися папки зі знайденими розширеннями
dest_folder = 'sorted'
sort_files(folder_path, dest_folder)
    