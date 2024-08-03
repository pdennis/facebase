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

def process_image(image_path, face_detector, recognition_model, confidence_threshold=0.7):
    try:
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize image if it's too large
        max_size = 1000
        height, width = img_rgb.shape[:2]
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            img_rgb = cv2.resize(img_rgb, None, fx=scale, fy=scale)
        
        # Detect faces using MTCNN
        faces = face_detector.detect_faces(img_rgb)
        if not faces:
            print(f"No face detected in {image_path}")
            return None

        embeddings = []
        for face_data in faces:
            confidence = face_data['confidence']
            if confidence < confidence_threshold:
                continue
            
            # Extract face area
            x, y, width, height = face_data['box']
            face_img = img_rgb[y:y+height, x:x+width]
            
            # You might want to add face alignment here
            # aligned_face = align_face(face_img, face_data['keypoints'])
            
            # Generate embedding
            embedding = DeepFace.represent(img_path=face_img, model_name=recognition_model, enforce_detection=False)
            embeddings.append(np.array(embedding[0]['embedding'], dtype=np.float64))
        
        return embeddings

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def find_matches(folder_path, embeddings_dict, threshold=0.5, recognition_model="Facenet512", confidence_threshold=0.7):
    matches = []
    face_detector = MTCNN()
    
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if os.path.isfile(image_path):
            new_embeddings = process_image(image_path, face_detector, recognition_model, confidence_threshold)
            if new_embeddings is None or len(new_embeddings) == 0:
                continue
            
            for new_embedding in new_embeddings:
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
    
    # Set parameters (you might want to make these configurable via command line arguments)
    similarity_threshold = 0.5
    face_detection_confidence = 0.7
    recognition_model = "Facenet512"
    
    # Find matches in the folder
    matches = find_matches(folder_path, embeddings_dict, 
                           threshold=similarity_threshold, 
                           recognition_model=recognition_model, 
                           confidence_threshold=face_detection_confidence)
    
    # Print summary of matches
    if matches:
        print("\nSummary of Matches:")
        for match in matches:
            print(f"Image: {match['image_path']}, Person: {match['person_name']}, "
                  f"Description: {match['person_description']}, Similarity: {match['similarity']:.4f}")
    else:
        print("No matches found.")