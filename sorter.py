import click
import eyed3
import os
import shutil

@click.command()
@click.option('-s', '--src-dir', default='.', help='Source directory.', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Destination directory.', show_default=True)
def music_sort(src_dir, dst_dir):
    while True:
        if os.path.isdir(src_dir):
            try:
                t = os.scandir(src_dir)
            except PermissionError as e:
                print(str(e))
                print('Введите путь к другой директории. Для выхода нажмите q')
                src_dir = input('> ')
                if src_dir == 'q':
                    break
            else:
                with t:
                    for entry in t:
                        if not entry.name.startswith('.') and entry.is_file() \
                                and entry.name.lower().endswith('.mp3'):
                            try:
                                audiofile = eyed3.load(entry)
                                if not audiofile.tag.title:
                                    title = entry.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Не хватает тегов для сортировки: {entry.name}')
                                    continue
                                else:
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')

                                audiofile.tag.save()
                            except AttributeError as e:
                                print(f'Что-то не так с файлом: {entry.name}')
                            except PermissionError as e:
                                print(f'Нет прав для изменения файла: {entry.name}')
                                continue
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, entry.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))

                                else:
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as e:
                                        print(str(e))
                                        print('Введите путь к другой директории. Для выхода нажмите q')
                                        dst_dir = input('>>> ')
                                        if dst_dir == 'q':
                                            break
                                    else:
                                        shutil.move(os.path.join(src_dir, entry.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, entry.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                print('Done')
                break
        else:
            print('Источник директории не найден')
            print('Введите путь к другой директории. Для выхода нажмите q')
            src_dir = input('>>> ')
            if src_dir == 'q':
                break

if __name__ == '__main__':
    music_sort()