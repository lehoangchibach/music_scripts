import os

from moviepy.editor import *
from pytube import YouTube


# Step 1: Download the YouTube video in the highest available audio quality
def download_youtube_video(video_url, output_path="video.mp4"):
    yt = YouTube(video_url)
    video_stream = yt.streams.filter(file_extension="mp4").first()
    video_stream.download(filename=output_path)
    print(f"Downloaded: {output_path}")


# Step 2: Convert the video file to MP3 with desired bitrate
def convert_to_mp3(video_file, mp3_output="output.mp3", bitrate="192k"):
    video = VideoFileClip(video_file)

    # Export audio with the specified bitrate
    print(f"Converting to MP3 with bitrate: {bitrate}")
    audio_output_path = mp3_output
    video.audio.write_audiofile(audio_output_path, codec="mp3", bitrate=bitrate)

    video.close()
    print(f"Converted to MP3: {audio_output_path}")


# Step 3: Clean up the video file after conversion (optional)
def clean_up_temp_files(video_file):
    if os.path.exists(video_file):
        os.remove(video_file)
        print(f"Temporary file {video_file} removed.")


# Example usage:
video_url = "https://youtu.be/xrG7z1Xqskk?si=g23bfnjCd46XMiB3"  # Replace with actual YouTube URL
video_file = "outputs/downloaded_video.mp4"
mp3_output_file = "outputs/output_audio.mp3"
desired_bitrate = "320k"  # Set the MP3 quality (e.g., 128k, 192k, 320k)

download_youtube_video(video_url, video_file)
convert_to_mp3(video_file, mp3_output_file, bitrate=desired_bitrate)

# Optionally remove the video file after conversion
clean_up_temp_files(video_file)
