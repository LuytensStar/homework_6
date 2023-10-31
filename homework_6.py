import os
import shutil
from pathlib import Path
import re
images = []
documents = []
musics = []
videos = []
archives = []
def normalize(path):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    p = Path(directory)
    for k in p.iterdir():
        if k.is_dir() == False:
            filename = k.name
            m = re.sub('[@#!+~`№$:^&?*()]', '_', filename)
            my_dest = m
            my_source = directory + '/' + filename
            my_dest = directory + '/' + my_dest
            os.rename(my_source, my_dest)
            print(filename)
            j = m.translate(TRANS)
            my_dest = j
            my_source = directory + '/' + m
            my_dest = directory + '/' + my_dest
            os.rename(my_source,my_dest)

def sort_files(directory):
    os.chdir(directory)
    normalize(directory)
    image_extensions = ('jpeg', 'jpg', 'png', 'svg')
    video_extensions = ('avi', 'mp4', 'mov', 'mkv')
    document_extensions = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
    music_extensions = ('mp3', 'ogg', 'wav', 'amr')
    archive_extensions = ('zip', 'gz', 'tar')

    known_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_extension = filename.split('.')[-1].lower()

            if file_extension in image_extensions:
                images.append(filename)
                destination = 'images'
                known_extensions.add(file_extension)
                images.append(filename)
            elif file_extension in video_extensions:
                videos.append(filename)
                destination = 'videos'
                known_extensions.add(file_extension)
            elif file_extension in document_extensions:
                documents.append(filename)
                destination = 'documents'
                known_extensions.add(file_extension)
            elif file_extension in music_extensions:
                musics.append(filename)
                destination = 'audio'
                known_extensions.add(file_extension)
            elif file_extension in archive_extensions:
                archives.append(filename)
                destination = 'archives'
                archive_path = os.path.join(root, filename)
                archive_folder = os.path.join(root, filename)
                shutil.unpack_archive(archive_path, archive_folder)
            else:
                destination = 'unknown'
                unknown_extensions.add(file_extension)

            destination_directory = os.path.join(root, destination)
            os.makedirs(destination_directory, exist_ok=True)
            new_file_path = os.path.join(destination_directory, filename)
            shutil.move(os.path.join(root, filename), new_file_path)

        # Видалення порожніх папок
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    print("Відомі розширення файлів:", ', '.join(known_extensions))
    print("Невідомі розширення файлів:", ', '.join(unknown_extensions))
    print('Документи: ', documents)
    print('Музика: ', musics)
    print('Відео: ', videos)
    print('Зображення: ', images)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Напишіть:sort.py <папка>")
        sys.exit(1)
    directory = sys.argv[1]
    sort_files(directory)
