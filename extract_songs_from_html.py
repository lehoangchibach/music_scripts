cnt = 0
with open("G:\\Musics\\scripts\\outputs\\YouTube Music.txt", "r") as f:
    data = f.read()
    # data = f.readline()
    # while data:
    #     print(data)
    #     # if '<dom-if class="style-scope ytmusic-two-row-item-renderer"><template is="dom-if"></template></dom-if>' in data:
    #     cnt += 1
    #     print(cnt)
    #     data = f.readline()


from bs4 import BeautifulSoup

soup = BeautifulSoup(data)
table = soup.find_all(
    "yt-formatted-string",
    {"class": "title style-scope ytmusic-responsive-list-item-renderer complex-string"},
)
songs = [entry["title"] for entry in table][:-7]
print(f"Total songs: {len(songs)}")
with open("G:\\Musics\\scripts\\outputs\\exp_songs.txt", "w") as f:
    f.write("\n".join(songs))
