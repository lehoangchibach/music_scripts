import os
import shutil


def move_files_from_subfolders(source_folder, target_folder):
    # Create the target folder if it does not exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Walk through all directories and subdirectories in the source folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_folder, file)

            # Ensure we do not overwrite files with the same name
            if os.path.exists(target_file_path):
                base, extension = os.path.splitext(file)
                i = 1
                print(extension)
                if extension not in {"flac", "mp3", "m4a", "wav"}:
                    continue
                new_target_file_path = os.path.join(
                    target_folder, f"{base}_{i}{extension}"
                )
                while os.path.exists(new_target_file_path):
                    i += 1
                    new_target_file_path = os.path.join(
                        target_folder, f"{base}_{i}{extension}"
                    )
                target_file_path = new_target_file_path

            # Move the file
            shutil.move(source_file_path, target_file_path)
            print(f"Moved: {source_file_path} -> {target_file_path}")


if __name__ == "__main__":
    source_folder = "/home/lehoangchibach/Downloads/torrents/nicotine"
    target_folder = "/home/lehoangchibach/Music/files/tmp"
    move_files_from_subfolders(source_folder, target_folder)
