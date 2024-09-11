import difflib
import os


def read_songs(directory):
    with open(directory, "r") as f:
        songs = f.readlines()

    songs = [song.strip() for song in songs if song[0] != "#"]
    return songs


def find_similar_files(names, directory):
    # List all files in the directory
    files_in_directory = os.listdir(directory)
    files_in_directory = [file.lower() for file in files_in_directory]
    # Dictionary to hold the result
    similar_files = {}

    for name in names:
        # Find close matches for the name in the files
        matches = difflib.get_close_matches(
            name.lower(), files_in_directory, cutoff=0.6
        )
        if matches:
            similar_files[name] = matches
        else:
            similar_files[name] = []

    return similar_files


def write_unfound(files, directory):
    content = "\n".join(files)
    with open(directory, "w") as f:
        f.writelines(content)


def write_found(files, directory):
    # lines = [a + ' ' + str(b) for a, b in zip(files, matches)]
    content = "\n".join(files)
    with open(directory, "w") as f:
        f.writelines(content)


# Example usage
names_to_check = read_songs("G:\\Musics\\scripts\\outputs\\songs.txt")
directory_path = "G:\\Musics\\files"
unfound_path = "G:\\Musics\\scripts\\outputs\\unfound.txt"
found_path = "G:\\Musics\\scripts\\outputs\\found.txt"

similar_files = find_similar_files(names_to_check, directory_path)

# Print the results
not_found = []
found = []
for name, matches in similar_files.items():
    if matches:
        found.append(name + ": -----" + str(matches))
        print(f"Files similar to '{name}': {matches}")
    else:
        not_found.append(name)

write_unfound(not_found, unfound_path)
write_found(found, found_path)

print(f"Found: {len(found)}")
print(f"Not found: {len(not_found)}")
