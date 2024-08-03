# FaceBase: Simple Face Recognition System

FaceBase is a straightforward, Python-based face recognition system that allows you to store face embeddings in a database and perform facial recognition on new images.

I will likely make a verison of this with a user interface for my team; as described here, you'll need to be somewhat familiar with running python scripts on your computer in order to get it working. If you're on a mac and you don't offhand know whether a command should be run as python or python3, you've got some reading to do before you're ready to get this working. 

## Features

- Robust face detection using MTCNN
- Advanced face recognition using Facenet512
- SQLite database for storing face embeddings
- Easy-to-use scripts for adding faces and performing recognition

## Quick Start

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add faces to the database:
   ```
   python faceloader.py
   ```

3. Perform face recognition:
   ```
   python facesearch.py
   ```

## How It Works

First you'll want to take some images of the person you're searching for, crop them to be tight shots of the persons face, put them all in one folder,  and feed them to faceloader.py

`faceloader.py` detects faces in images, generates embeddings, and stores them in a SQLite database.

Then, once they've been digested by faceloader.py and added to the database (you can add multiple people), you'll want to use facesearch.py to do the search. It will just ask you which folder it should look in.

 `facesearch.py` processes new images, generates embeddings, and compares them against stored embeddings to find matches.

## Customization

- Adjust threshold values in the scripts to fine-tune detection and matching sensitivity.
- Modify the database schema in `faceloader.py` to store additional information.

## Note

Ensure you have the necessary rights to use and store facial data, and always use this system responsibly and ethically.

## Bonus script

I added a script called videoexploder.py here. To use it, you'll need to install ffmpeg and yt-dlp 

on a Mac with homebrew, that would be `brew install ffmpeg` and `brew install yt-dlp`. 

What it's for is, if you'd like to search an online video to see if somebody appears in it (say, a CSPAN committee hearing and you're tryin to confirm attendance) you can enter the link of the video. The script will download it and explode it into images of every 2 seconds of video. You can then use the other scripts in this repo to search for the person you're trying to find (or not find, such as it may be).
