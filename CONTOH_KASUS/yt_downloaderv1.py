import yt_dlp
import os
import unicodedata

# Define the path to yt_dlp.exe
# yt_dlp_path = 'D:\\yt_dlp\\yt_dlp.exe'
yt_dlp_path = r'D:\yt_dlp\yt_dlp.exe'

# Define the path to ffmpeg.exe
# ffmpeg_path = 'D:\\yt_dlp\\ffmpeg-full_build\\bin\\ffmpeg.exe'
ffmpeg_path = r'D:\yt_dlp\ffmpeg-full_build\bin\ffmpeg.exe'

# Define the playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLlCrV9TCfzMaIDYlwykvUEnji83s_Jm8G"
# playlist_url = "https://www.youtube.com/shorts/NHquaDS6XQ0"

# Define the download location

download_location = r'D:\yt_dlp'

# Define the yt_dlp options
ydl_opts = {
    'ignoreerrors': True,
    'format': 'bestvideo[height=720]+bestaudio[ext=m4a]/best[height=720]', # REGULAR VIDEOS
    # 'format': 'bv*+ba/b', # SHORT VIDEOS
    'merge_output_format': 'mp4',
    'outtmpl': f'{download_location}/%(playlist_title)s/%(title)s.%(ext)s',
    'download_archive': f'{download_location}/downloaded.txt',
    'playlist_items': '34-36', # REGULAR VIDEOS
    # 'playlist_items': None, # SHORT VIDEOS
    'ffmpeg_location': ffmpeg_path
}

# Create the yt_dlp object
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # # Set the path to yt_dlp.exe
    # ydl.exe = yt_dlp_path

    # Get the playlist info
    info = ydl.extract_info(playlist_url, download=False)

    # Download the video files
    ydl.download([playlist_url])