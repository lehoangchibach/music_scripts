import os

from moviepy.editor import VideoFileClip
from pytube import YouTube


# Step 1: Download the YouTube video in the highest available audio quality
def download_youtube_video(video_url, output_path="video.mp4"):
    yt = YouTube(video_url)
    print(yt.streams.filter(only_audio=True))

    video_stream = yt.streams.filter(only_audio=True)
    itag, max_abr = None, -1
    for stream in video_stream:
        if int(stream.abr[:-4]) > max_abr:
            itag = stream.itag
    yt.streams.get_by_itag(itag).download(filename=output_path)
    print(f"Downloaded: {output_path}")
    exit()


# Step 2: Convert the video file to MP3 with desired bitrate
def convert_to_mp3(video_file, mp3_output="output.mp3", bitrate="192k"):
    video = VideoFileClip(video_file)
    # Export audio with the specified bitrate
    print(f"Converting to MP3 with bitrate: {bitrate}")
    if not video or not video.audio:
        raise BaseException("video None")

    video.audio.write_audiofile(mp3_output, codec="mp3", bitrate=bitrate)

    video.close()
    print(f"Converted to MP3: {mp3_output}")


# Step 3: Clean up the video file after conversion (optional)
def clean_up_temp_files(video_file):
    if os.path.exists(video_file):
        os.remove(video_file)
        print(f"Temporary file {video_file} removed.")


# Example usage:
video_url = input("URL: ")

video_file = "outputs/downloaded_video.mp4"
mp3_output_file = "outputs/output_audio.mp3"
desired_bitrate = "320k"  # Set the MP3 quality (e.g., 128k, 192k, 320k)

download_youtube_video(video_url, video_file)
convert_to_mp3(video_file, mp3_output_file, bitrate=desired_bitrate)

# Optionally remove the video file after conversion
clean_up_temp_files(video_file)
