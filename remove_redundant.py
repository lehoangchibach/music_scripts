import os
from urllib.parse import unquote

with open("./ip") as f:
    data = f.readlines()

song_names = set()
for s in data:
    s = s.strip()
    song = s.split("/")[-1]
    song = unquote(song)
    song_names.add(song)

cnt = 0
local_path = "../Music/files/Rocks_normalized/"
song_locals = os.listdir(local_path)
for i in song_locals:
    if i not in song_names:
        cnt += 1
        os.remove(f"{local_path}/{i}")

print(len(song_locals), len(song_names))
print(cnt)
