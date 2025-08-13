import multiprocessing
import os
import random
import shutil
import sys
from functools import partial

from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3, TALB, TCON, TDRC, TIT2, TPE1
from mutagen.mp3 import MP3
from pydub import AudioSegment


def handle_metadata(flac_path, mp3_path):
    flac_metadata = FLAC(flac_path)

    # Create an MP3 file object to add metadata
    mp3_metadata = MP3(mp3_path, ID3=ID3)

    # Add ID3 tag if it doesn't exist
    try:
        mp3_metadata.add_tags()
    except:
        pass

    # Transfer metadata from FLAC to MP3
    for tag in flac_metadata.keys():
        if tag == "title":
            mp3_metadata.tags.add(TIT2(encoding=3, text=flac_metadata[tag]))
        elif tag == "artist":
            mp3_metadata.tags.add(TPE1(encoding=3, text=flac_metadata[tag]))
        elif tag == "album":
            mp3_metadata.tags.add(TALB(encoding=3, text=flac_metadata[tag]))
        elif tag == "genre":
            mp3_metadata.tags.add(TCON(encoding=3, text=flac_metadata[tag]))
        elif tag == "date":
            mp3_metadata.tags.add(TDRC(encoding=3, text=flac_metadata[tag]))

    for picture in flac_metadata.pictures:
        mp3_metadata.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime=picture.mime,  # image/jpeg or image/png
                type=3,  # 3 is for the cover (front) image
                desc="Cover",
                data=picture.data,
            )
        )

    # Save the MP3 file with metadata
    mp3_metadata.save()


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
                dst_file = os.path.join(
                    dst_folder, f"{os.path.splitext(filename)[0]}.mp3"
                )
                if os.path.isfile(dst_file):
                    print(f"EXIST: {filename}")
                    continue

                # Load the FLAC file
                audio = AudioSegment.from_file(src_file, format="flac")
                # Export as MP3 with the specified bitrate
                audio.export(
                    dst_file,
                    format="mp3",
                    bitrate=bitrate,
                    parameters=["-ac", "2", "-ar", "48000"],
                )
                handle_metadata(src_file, dst_file)

                cnt_convert += 1
                print(f"SUCCESS - {os.getpid()}: {src_file} to {dst_file}")
            except BaseException as e:
                print(f"FAILED - {os.getpid()}: {src_file}")
                print(f"ERROR - {os.getpid()}: {e}")
                errs.append(filename)

        else:
            dst_file = os.path.join(dst_folder, filename)
            if os.path.isfile(dst_file):
                print(f"EXIST: {filename}")
                continue

            shutil.copy2(src_file, dst_folder)
            cnt_cp += 1
            print(f"COPY - {os.getpid()}: {src_file} to {dst_folder}")

    print(f"SUCCESS: {cnt_convert}")
    print(f"COPY: {cnt_cp}")
    print(f"Total: {cnt_convert + cnt_cp}")
    print(f"FAIL: {os.getpid()}: {len(errs), errs}")
    sys.stdout.flush()


def divide_list(lst, n):
    random.shuffle(lst)
    chunk_size = len(lst) // n
    chunk_end = n * chunk_size
    remainder = len(lst) % n
    res = [lst[i : i + chunk_size] for i in range(0, chunk_end, chunk_size)]
    for i in range(remainder):
        res[i].append(lst[chunk_end + i])
    return res


# Set your source and destination folders
src_folder = "../files/Rocks_normalized"
dst_folder = "../files/Rocks_compressed"
NUM_PROCESS = 12

if __name__ == "__main__":
    files = os.listdir(src_folder)
    divided_files = divide_list(files, NUM_PROCESS)

    with multiprocessing.Pool(processes=NUM_PROCESS) as pool:
        func = partial(
            convert_flac_to_mp3, src_folder=src_folder, dst_folder=dst_folder
        )
        results = pool.map(func, divided_files)
        print(results)
