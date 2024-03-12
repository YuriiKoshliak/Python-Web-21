import sys
import re
import shutil
import gzip
import os
from pathlib import Path

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

folders_to_create = ["images", "documents", 'audio', 'video', 'archives', 'other']
images = ['.JPEG', '.PNG', '.JPG', '.SVG']
documents = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
audio = ['.MP3', '.OGG', '.WAV', '.AMR']
video = ['.AVI', '.MP4', '.MOV', '.MKV']
archives = ['.ZIP', '.GZ', '.TAR']
found_extensions = set()
found_images = []
found_documents = []
found_audio = []
found_video = []
found_archives = []
found_other = []

# Removes empty directories from a specified path
def delete_empty_folders(path):
    deleted = set()
    
    for current_dir, subdirs, files in os.walk(path, topdown=False):
        still_has_subdirs = False
        for subdir in subdirs:
            if os.path.join(current_dir, subdir) not in deleted:
                still_has_subdirs = True
                break
    
        if not any(files) and not still_has_subdirs:
            os.rmdir(current_dir)
            deleted.add(current_dir)
    print(f'The following empty folders were deleted: {deleted}\n' if len(deleted) != 0 else "No empty folders found\n")

# Standardizes filenames by replacing non-alphanumeric characters.
def normalize(name):
    try:
        base, extension = name.rsplit('.', 1)
        trans_name = base.translate(TRANS)
        good_name = re.sub(r'\W', "_", trans_name)
        return f'{good_name}.{extension}'
    except ValueError:
        trans_name = name.translate(TRANS)
        return re.sub(r'\W', "_", trans_name)
     
# Extracts contents of an archive to a specified directory.
def unpack(archive_path, path_to_unpack):
    shutil.unpack_archive(archive_path, path_to_unpack)

# Sorts and organizes files by type, handles archives.
def move_rename_file(path):
    from src.handlers import main_folder_path
    k = 1
    extension = path.suffix
    base = normalize(path.stem)
    new_name = normalize(path.name)

    if extension.upper() in images:
        new_folder = "images"
        found_images.append(path.name)
    elif extension.upper() in documents:
        new_folder = "documents"
        found_documents.append(path.name)
    elif extension.upper() in audio:
        new_folder = "audio"
        found_audio.append(path.name)
    elif extension.upper() in video:
        new_folder = "video"
        found_video.append(path.name)
    elif extension.upper() in archives:
        if extension.upper() == '.GZ':
            try:
                with gzip.open(path, 'rb') as f_in:
                    os.mkdir(main_folder_path / 'archives' / base )
                    with open(main_folder_path / 'archives' / base / base, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                found_archives.append(path.name)        
                os.remove(path)
            except FileExistsError:
                print(f'The archive {path} ould not be unpacked because the folder {base} already exists.\n')
        else:
            unpack(path, main_folder_path / 'archives' / base)
            found_archives.append(path.name) 
            os.remove(path)

        return None
        
    else:
        new_folder = "other"
        found_extensions.add(extension.upper())
        found_other.append(path.name) 

    new_file_path = main_folder_path / new_folder / new_name

# Attempts to rename a file, retries with incremented suffix on error.
    def cykle_try(new_file_path):
        nonlocal k
        try:
            path.rename(new_file_path)
        except FileExistsError:
            k += 1
            print (f'The file {new_file_path.name} already exists in the folder {new_folder}, the name will be changed to {base}{k}\n')
            mega_name = new_file_path.with_stem(f'{base}{k}')
            try:
                path.rename(mega_name)
            except FileExistsError:
                cykle_try(mega_name.with_stem(f'{base}{k}'))

    cykle_try(new_file_path)

# Recursively sorts files and directories using custom rules.
def monster_sort(path):
    for element in path.iterdir():
        if element.name not in folders_to_create:
            if element.is_dir():
                monster_sort(element)
            else:
                move_rename_file(element)
                
# Initializes sorting process, creates folders, and sorts files.
def sorting():
        from src.handlers import main_folder_path  
        for folder_name in folders_to_create:
            try:
                (main_folder_path / folder_name).mkdir()
            except FileExistsError:
                ...
        
        monster_sort(main_folder_path)
        delete_empty_folders(main_folder_path)
        print(f'Strange extensions were found in the folder: {found_extensions}.\
 For your safety, all such files {found_other} have been moved to the “other” folder.\n' if len(found_extensions) != 0 else "")
        print(f'''Sorted files: 
              
              images: {found_images} 

              video files: {found_video} 

              documents: {found_documents} 

              music: {found_audio} 

              archives: {found_archives} \n''')
        
        return "Sorting was completed successfully"

if __name__ == "__main__":
    sorting()



