import os
import shutil
from pydub import AudioSegment

def convert_flac_to_mp3(src_folder, dst_folder, bitrate="320k"):
    # Ensure the destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Loop through all files in the source folder
    cnt_convert, cnt_cp = 0, 0 
    errs = []
    for filename in os.listdir(src_folder):
        if cnt_convert + cnt_cp >= 20:
            break
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
                print(f"SUCCESS{src_file} to {dst_file}")
            except BaseException as e:
                print(f"ERROR: {e}")
                print(f"FAILED: {src_file}")
                errs.append(filename)

        else:
            shutil.copy2(src_file, dst_folder)
            cnt_cp += 1
            print(f"COPY {src_file} to {dst_folder}")
    
    print(f"SUCCESS: {cnt_convert}")
    print(f"COPY: {cnt_cp}")
    print(f"Total: {cnt_convert + cnt_cp}")
    print(f"FAILED: {len(errs), errs}")

# Set your source and destination folders
src_folder = "C:\\Users\\lehoa\\OneDrive\\Documents\\Musics\\files\\Rocks"
dst_folder = "C:\\Users\\lehoa\\OneDrive\\Documents\\Musics\\files\\Rocks_compressed"

convert_flac_to_mp3(src_folder, dst_folder)