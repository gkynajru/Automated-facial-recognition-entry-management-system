import face_recognition
import cv2
import numpy as np
import pickle
from datetime import datetime
import os
from .data_manager import DataManager

__all__ = ['FaceRecognizer']

class FaceRecognizer:
    def __init__(self):
        # Use absolute path for encodings file
        self.encodings_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'data', 
            'encodings.pickle'
        )
        self.known_encodings = []
        self.known_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.face_id = []
        self.process_current_frame = True
        self.load_encodings()
        self.data_manager = DataManager()

    def load_encodings(self):
        try:
            with open(self.encodings_file, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]
            print("Encodings loaded successfully")
        except Exception as e:
            print(f"Error loading encodings: {e}")

    def _face_confidence(self, face_distance, face_match_threshold=0.4):
        range_val = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range_val * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + '%'
        else:
            value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

    def process_frame(self, frame):
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Only process every other frame
        if self.process_current_frame:
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            self.face_ids = []  # Add this line to store IDs
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.4)
                name = "Unknown"
                confidence = "Unknown"
                display_name = "Unknown"
                person_id = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    person_id = self.known_names[first_match_index]  # This is the ID
                    member_info = self.data_manager.get_member_info(person_id)
                    if member_info and "Full name" in member_info:
                        display_name = member_info["Full name"]
                    face_distances = face_recognition.face_distance([self.known_encodings[first_match_index]], face_encoding)
                    confidence = self._face_confidence(face_distances[0])

                self.face_names.append((display_name, confidence))
                self.face_ids.append(person_id)  # Store the ID

        self.process_current_frame = not self.process_current_frame

        # Draw results
        for (top, right, bottom, left), (name, confidence) in zip(self.face_locations, self.face_names):
            # Scale back coordinates
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw box and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            label = f'{name} ({confidence})'
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        return frame, self.face_names, self.face_ids  # Return IDs as well

    def get_recognized_ids(self):
        """Return list of recognized person IDs"""
        return [name for name, _ in self.face_names if name != "Unknown"]
