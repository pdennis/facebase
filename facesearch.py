import os
import sqlite3
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity
from mtcnn import MTCNN
import cv2

def cosine_sim(a, b):
    return cosine_similarity([a], [b])[0][0]

def load_average_embeddings(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT 
            person_id, 
            name, 
            description, 
            average_embedding 
        FROM 
            averaged_embeddings
    """)
    data = c.fetchall()
    conn.close()
    
    embeddings_dict = {}
    for row in data:
        person_id, name, description, embedding_blob = row
        embedding = np.frombuffer(embedding_blob, dtype=np.float64)
        embeddings_dict[person_id] = {'name': name, 'description': description, 'embedding': embedding}
    return embeddings_dict

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

def find_matches(folder_path, embeddings_dict, threshold=0.5, recognition_model="Facenet512"):
    matches = []
    face_detector = MTCNN()
    
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if os.path.isfile(image_path):
            new_embedding = process_image(image_path, face_detector, recognition_model)
            if new_embedding is None:
                continue
            
            for person_id, person_data in embeddings_dict.items():
                stored_embedding = person_data['embedding']
                similarity = cosine_sim(new_embedding, stored_embedding)
                
                if similarity > threshold:
                    matches.append({
                        'image_path': image_path,
                        'person_name': person_data['name'],
                        'person_description': person_data['description'],
                        'similarity': similarity
                    })
                    print(f"Match found in {image_path} for {person_data['name']} (Similarity: {similarity:.4f})")
    
    return matches

# Main script execution
if __name__ == "__main__":
    # Database path
    db_path = "face_recognition.db"
    
    # Load stored average embeddings
    embeddings_dict = load_average_embeddings(db_path)
    
    # Folder containing images to check
    folder_path = input("Enter the folder path containing the images to check: ")
    
    # Find matches in the folder
    matches = find_matches(folder_path, embeddings_dict)
    
    # Print summary of matches
    if matches:
        print("\nSummary of Matches:")
        for match in matches:
            print(f"Image: {match['image_path']}, Person: {match['person_name']}, Description: {match['person_description']}, Similarity: {match['similarity']:.4f}")
    else:
        print("No matches found.")