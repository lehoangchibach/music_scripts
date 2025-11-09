import os

from mutagen import MutagenError
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3


def get_audio_title(file_path):
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"

    try:
        if file_path.lower().endswith(".mp3"):
            audio = MP3(file_path, ID3=ID3)
            title = audio.get("TIT2")
            return (
                f"{title.text[0]}.mp3"
                if title
                else f"Error: Title tag not found - {file_path}"
            )
        elif file_path.lower().endswith(".flac"):
            audio = FLAC(file_path)
            title = audio.get("title")
            return (
                f"{title[0]}.flac"
                if title
                else f"Error: Title tag not found - {file_path}"
            )
        else:
            return f"Error: Unsupported file format - {file_path}"
    except MutagenError as e:
        return f"Error reading file: {e}"


def update_name(directory):
    files_in_directory = os.listdir(directory)
    files_in_directory = [os.path.join(directory, file) for file in files_in_directory]

    for file in files_in_directory:
        song_title = get_audio_title(file)
        if song_title[:5] == "Error":
            continue
        new_name = os.path.join(directory, song_title)
        new_name = new_name.replace("'", "_")

        try:
            if os.path.isfile(file):  # Check if it's a file before renaming
                os.rename(file, new_name)
                print(f"Successfully renamed {file} to {new_name}")
        except OSError as e:
            print(f"Error renaming {file}: \n{e}")


directory_path = "../files/tmp"

update_name(directory_path)
