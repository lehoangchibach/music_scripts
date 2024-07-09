import os


def count_files_in_folder(folder_path):
    file_count = 0

    # Walk through all directories and subdirectories in the folder
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)

    return file_count


if __name__ == "__main__":
    folder_path = "../files/Rocks"  # Replace with the path to your folder
    total_files = count_files_in_folder(folder_path)
    print(f"Total number of files in the folder '{folder_path}': {total_files}")
