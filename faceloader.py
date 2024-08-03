import os
import sqlite3
import numpy as np
from deepface import DeepFace
from mtcnn import MTCNN
import cv2

# Function to create the database and tables if they don't exist
def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS people
                 (person_id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS embeddings
                 (embedding_id INTEGER PRIMARY KEY, person_id INTEGER, embedding BLOB, image_path TEXT,
                  FOREIGN KEY(person_id) REFERENCES people(person_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS averaged_embeddings
                 (person_id INTEGER PRIMARY KEY, name TEXT, description TEXT, average_embedding BLOB,
                  FOREIGN KEY(person_id) REFERENCES people(person_id))''')
    conn.commit()
    conn.close()

# Function to detect face and generate embedding
def process_image(image_path, face_detector, recognition_model):
    try:
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect face using MTCNN
        faces = face_detector.detect_faces(img_rgb)
        if not faces:
            print(f"No face detected in {image_path}")
            return None

        # Get the first detected face
        face_data = faces[0]
        confidence = face_data['confidence']

        if confidence < 0.9:
            print(f"Low confidence face detection in {image_path}")
            return None

        # Extract face area
        x, y, width, height = face_data['box']
        face_img = img[y:y+height, x:x+width]

        # Generate embedding
        embedding = DeepFace.represent(img_path=face_img, model_name=recognition_model, enforce_detection=False)
        return np.array(embedding[0]['embedding'], dtype=np.float64)

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

# Function to store person's information and embeddings in the database
def store_embeddings(folder_path, name, description, db_path, recognition_model="Facenet512"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Insert person information
    c.execute("INSERT INTO people (name, description) VALUES (?, ?)", (name, description))
    person_id = c.lastrowid
    
    embeddings_list = []
    face_detector = MTCNN()

    # Process each image in the folder
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if os.path.isfile(image_path):
            embedding = process_image(image_path, face_detector, recognition_model)
            if embedding is not None:
                embeddings_list.append(embedding)
                embedding_blob = sqlite3.Binary(embedding.tobytes())
                
                # Store embedding in the database
                c.execute("INSERT INTO embeddings (person_id, embedding, image_path) VALUES (?, ?, ?)",
                          (person_id, embedding_blob, image_path))
                print(f"Stored embedding for {image_path}")

    # Calculate the average embedding for the person
    if embeddings_list:
        average_embedding = np.mean(embeddings_list, axis=0)
        average_embedding_blob = sqlite3.Binary(average_embedding.tobytes())
        # Store the average embedding in the database
        c.execute("INSERT INTO averaged_embeddings (person_id, name, description, average_embedding) VALUES (?, ?, ?, ?)",
                  (person_id, name, description, average_embedding_blob))
        print(f"Stored average embedding for {name}")

    conn.commit()
    conn.close()
    print(f"All embeddings stored for {name}.")

# Main script execution
if __name__ == "__main__":
    # Database path
    db_path = "face_recognition.db"
    # Create database and tables if they don't exist
    create_database(db_path)
    # Input person's name and description
    name = input("Enter the person's name: ")
    description = input("Enter a brief description of the person: ")
    # Folder containing images of the person
    folder_path = input("Enter the folder path containing the images: ")
    # Store the embeddings in the database
    store_embeddings(folder_path, name, description, db_path)