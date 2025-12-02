import face_recognition
import requests
import numpy as np
from io import BytesIO
from PIL import Image

def load_target_face(image_path):
    """
    Loads the user's uploaded image from a local path and returns its face encoding.
    """
    print(f"Loading target face from: {image_path}")
    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            return encodings[0]
        else:
            print("Error: No face found in the target image.")
            return None
    except Exception as e:
        print(f"Error loading target face: {e}")
        return None

def download_and_verify_image(url):
    """
    Downloads an image from a URL into memory.
    Returns a numpy array of the image if successful, None otherwise.
    """
    try:
        # Set a timeout (10s) and valid User-Agent to avoid some 403s
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.convert('RGB')
            return np.array(img)
    except:
        pass
    return None

def check_match(target_encoding, image_url, tolerance=0.6):
    """
    Compares a scraped image against the target.
    ALWAYS returns a tuple: (bool, float)
    """
    unknown_image = download_and_verify_image(image_url)
    
    if unknown_image is None:
        return False, 0.0  # <-- FIX: Must return a tuple, not just False

    try:
        unknown_encodings = face_recognition.face_encodings(unknown_image)
        for unknown_encoding in unknown_encodings:
            results = face_recognition.compare_faces([target_encoding], unknown_encoding, tolerance=tolerance)
            if results[0]:
                face_distance = face_recognition.face_distance([target_encoding], unknown_encoding)[0]
                confidence = (1 - face_distance) * 100 
                return True, confidence 
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")

    return False, 0.0