# FaceBase: Simple Face Recognition System

FaceBase is a straightforward, Python-based face recognition system that allows you to store face embeddings in a database and perform facial recognition on new images.

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

First you'll want to take some images of the person you're searching for, and feed them to faceloader.py
`faceloader.py` detects faces in images, generates embeddings, and stores them in a SQLite database.
Then, once they've been digested by faceloader.py and added to the database (you can add multiple people), you'll want to use facesearch.py to do the search. It will just ask you which folder it should look in.
 `facesearch.py` processes new images, generates embeddings, and compares them against stored embeddings to find matches.

## Customization

- Adjust threshold values in the scripts to fine-tune detection and matching sensitivity.
- Modify the database schema in `faceloader.py` to store additional information.

## Note

Ensure you have the necessary rights to use and store facial data, and always use this system responsibly and ethically.


