import os
import shutil

with open("./my file names.txt") as f:
    songs = f.readlines()

songs = {i.strip() for i in songs}

path = "../files/Rocks_compressed/"
dir_songs = os.listdir(path)
dir_songs = {song.rsplit(".", 1)[0]: os.path.join(path, song) for song in dir_songs}

for k, v in dir_songs.items():
    if k not in songs:
        shutil.copy2(v, "../files/iphone/")
