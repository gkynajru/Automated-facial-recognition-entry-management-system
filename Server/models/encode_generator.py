from imutils import paths
import face_recognition
import pickle
import cv2
import os

def encode_faces():
    # Get the path to the dataset directory
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset')
    
    # Get paths to all images in dataset
    print("[INFO] Finding images...")
    image_paths = list(paths.list_images(dataset_path))
    
    if not image_paths:
        print("[ERROR] No images found in dataset directory")
        return False

    # Initialize lists for encodings and names
    known_encodings = []
    known_names = []

    # Process each image
    total_images = len(image_paths)
    print(f"[INFO] Processing {total_images} images...")

    for (i, image_path) in enumerate(image_paths):
        # Extract person ID from the image path (folder name)
        print(f"[INFO] Processing image {i + 1}/{total_images}")
        person_id = image_path.split(os.path.sep)[-2]

        try:
            # Load and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                print(f"[WARNING] Could not read image: {image_path}")
                continue
                
            # Resize for faster processing
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces and compute encodings
            boxes = face_recognition.face_locations(rgb, model='hog')
            
            if not boxes:
                print(f"[WARNING] No face detected in {image_path}")
                continue
                
            # Compute facial embeddings
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            # Add encodings and IDs to lists
            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(person_id)

        except Exception as e:
            print(f"[ERROR] Failed to process {image_path}: {str(e)}")
            continue

    if not known_encodings:
        print("[ERROR] No valid encodings generated")
        return False

    # Save encodings to file
    print("[INFO] Serializing encodings...")
    data = {
        "encodings": known_encodings,
        "names": known_names
    }
    
    # Save to data directory
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'data',
        'encodings.pickle'
    )
    
    try:
        with open(output_path, "wb") as f:
            f.write(pickle.dumps(data))
        print(f"[SUCCESS] Saved encodings to {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save encodings: {str(e)}")
        return False

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs(os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'data'
    ), exist_ok=True)
    
    # Run encoding process
    if encode_faces():
        print("[INFO] Encoding process completed successfully")
    else:
        print("[ERROR] Encoding process failed")
