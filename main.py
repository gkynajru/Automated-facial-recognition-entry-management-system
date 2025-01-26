from flask import Flask, Response, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import cv2
import os
import time
import serial
import urllib.request
from datetime import datetime
import numpy as np

from models.face_recognizer import FaceRecognizer
from models.data_manager import DataManager

app = Flask(__name__)
socketio = SocketIO(app)
url = 'http://192.168.137.238/cam-hi.jpg'

# Initialize components
face_recognizer = FaceRecognizer()
data_manager = DataManager()

def serial_emit(i):
    ok = b'Welcome'
    eror = b'Error'
    ser = serial.Serial('COM5', baudrate= 9600)
    if i == 1:
        ser.write(ok)
    if i == 0:
        ser.write(eror)
    return ser

def generate_frames():
    while True:
        img_resp= urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgnp,-1)
        frame = cv2.resize(frame, (640, 480))

        # Process frame for face recognition
        processed_frame, recognized_faces, face_ids = face_recognizer.process_frame(frame)
        
        # Update recognition status using IDs
        if recognized_faces and face_ids:
            for i, (name, confidence) in enumerate(recognized_faces):
                person_id = face_ids[i]
                if person_id != "Unknown":
                    member_info = data_manager.get_member_info(person_id)
                    if member_info:
                        data_manager.update_attendance(person_id)
                        socketio.emit('faceRegCheck_update', {'peopleID': member_info})

        # Convert frame to bytes
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_webcam_frames():
    while True:
        img_resp= urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgnp,-1)
        frame = cv2.resize(frame, (640, 480))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/page0')
def page0():
    return render_template("page0.html")

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/webcam')
def webcam():
    return Response(
        generate_webcam_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        member_data = {
            "Full name": request.form.get('name'),
            "Age": request.form.get('age'),
            "Phone number": request.form.get('phone'),
            "Last attendance": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
        member_id = member_data["Phone number"][-4:]
        
        # Save member data to JSON
        if data_manager.add_member(member_id, member_data):
            # Set up camera and dataset path
            dataset_path = os.path.join(
                os.path.dirname(__file__),
                'dataset',
                member_id
            )
            os.makedirs(dataset_path, exist_ok=True)
            
            # Capture multiple photos
            cap = cv2.VideoCapture(0)
            print("Starting photo capture session...")
            for i in range(10):  # Take 10 photos
                time.sleep(0.5)  # Small delay between photos
                success, frame = cap.read()
                if success:
                    # Save image with timestamp to ensure unique names
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    image_path = os.path.join(dataset_path, f'image_{timestamp}.jpg')
                    cv2.imwrite(image_path, frame)
                    print(f"Captured photo {i+1}/10")
            
            cap.release()
            print("Photo capture complete")
            
            # Retrain face recognition model
            recognition_script = os.path.join(
                os.path.dirname(__file__),
                'models',
                'recognition.py'
            )
            try:
                os.system(f'python "{recognition_script}"')
                face_recognizer.load_encodings()
                print("Face recognition model updated successfully")
                return redirect(url_for('home'))  # Redirect to home page after successful signup
            except Exception as e:
                print(f"Error updating face recognition model: {e}")
            
    return render_template("page0.html")  # Only reaches here if there was an error

if __name__ == '__main__':
    socketio.run(app, debug=True)