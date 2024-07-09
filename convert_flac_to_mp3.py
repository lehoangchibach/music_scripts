import os
import shutil
from pydub import AudioSegment
import multiprocessing
from functools import partial
import random

def convert_flac_to_mp3(files, src_folder, dst_folder, bitrate="320k"):
    # Ensure the destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Loop through all files in the source folder
    cnt_convert, cnt_cp = 0, 0 
    errs = []
    for filename in files:
        # Check if the file is a FLAC file
        src_file = os.path.join(src_folder, filename)
        if filename.endswith(".flac"):
            try:
                dst_file = os.path.join(dst_folder, f"{os.path.splitext(filename)[0]}.mp3")

                # Load the FLAC file
                audio = AudioSegment.from_file(src_file, format="flac")
                # Export as MP3 with the specified bitrate
                audio.export(dst_file, format="mp3", bitrate=bitrate)

                cnt_convert += 1
                print(f"SUCCESS - {os.getpid()}: {src_file} to {dst_file}")
            except BaseException as e:
                print(f"ERROR - {os.getpid()}: {e}")
                print(f"FAILED - {os.getpid()}: {src_file}")
                errs.append(filename)

        else:
            shutil.copy2(src_file, dst_folder)
            cnt_cp += 1
            print(f"COPY - {os.getpid()}: {src_file} to {dst_folder}")
    
    print(f"SUCCESS: {cnt_convert}")
    print(f"COPY: {cnt_cp}")
    print(f"Total: {cnt_convert + cnt_cp}")
    print(f"FAILED - {os.getpid()}: {len(errs), errs}")


def divide_list(lst, n):
    random.shuffle(lst)
    chunk_size = len(lst)//n
    chunk_end = n * chunk_size
    remainder = len(lst) % n
    res = [lst[i:i + chunk_size] for i in range(0, chunk_end, chunk_size)]
    for i in range(remainder):
        res[i].append(lst[chunk_end+i])
    return res


# Set your source and destination folders
src_folder = "../files/Rocks"
dst_folder = "../files/Rocks_compressed"
NUM_PROCESS = 10

if __name__ == "__main__":
    files = os.listdir(src_folder)
    divided_files = divide_list(files, NUM_PROCESS)
    
    with multiprocessing.Pool(processes=NUM_PROCESS) as pool:
        func = partial(convert_flac_to_mp3, src_folder=src_folder, dst_folder=dst_folder)
        results = pool.map(func, divided_files)
        print(results)
