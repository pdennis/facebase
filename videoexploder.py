import os
import subprocess
import re

# Function to sanitize filename
def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

# Get video URL from user
video_url = input("Enter the YouTube video URL: ")

# Get video info
info_command = ['yt-dlp', '-J', video_url]
video_info = subprocess.check_output(info_command).decode('utf-8')
video_title = re.search(r'"title":\s*"([^"]+)"', video_info).group(1)

# Sanitize video title for use as folder name
folder_name = sanitize_filename(video_title)

# Create folder
os.makedirs(folder_name, exist_ok=True)

# Download video
download_command = ['yt-dlp', '-o', f'{folder_name}/video.%(ext)s', video_url]
subprocess.run(download_command)

# Find the downloaded video file
video_file = [f for f in os.listdir(folder_name) if f.startswith('video.')][0]
video_path = os.path.join(folder_name, video_file)

# Extract frames
extract_command = [
    'ffmpeg', 
    '-i', video_path, 
    '-vf', 'select=\'not(mod(n,60))\'',
    '-vsync', '0', 
    '-q:v', '2',
    f'{folder_name}/frame_%04d.jpg'
]

subprocess.run(extract_command)

print(f"Frames extracted to folder: {folder_name}")
