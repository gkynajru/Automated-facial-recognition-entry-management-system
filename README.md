# 🔐 Automated Facial Recognition Entry Management System

A smart entry management system using facial recognition technology to control access and manage attendance. The system combines embedded hardware control with AI-powered face detection for secure and automated entry management.

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org)
[![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![STM32](https://img.shields.io/badge/STM32-F4-03234B?style=flat&logo=stmicroelectronics&logoColor=white)](https://www.st.com/)
[![ESP32](https://img.shields.io/badge/ESP32-Camera-blue)](https://www.espressif.com/)

## 📊 Demo
[![Video Thumbnail](link_to_thumbnail_image)](https://youtu.be/uKJgqVJXqQI)
[![Demo Video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/uKJgqVJXqQI)

## ✨ Key Features

- Real-time facial recognition for access control
- Automated barrier gate control using servo motor
- LED display for user feedback and instructions
- Web interface for system monitoring and management
- New user registration with automated photo capture
- Secure database for storing member information
- Multi-component architecture for distributed processing

## 🔧 Components

### Hardware
- ESP32-CAM Module: Video streaming
- STM32F4 Board: System control
- I2C LCD Display: User feedback
- Micro Servo Motor: Gate control
- LED Indicators: Status display

### Software
- Face Recognition System: Python & OpenCV
- Web Interface: Flask & SocketIO
- Database: JSON-based storage
- Embedded Control: C/C++

## 📥 Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/gkynajru/Automated-facial-recognition-entry-management-system
```
2. **Install server dependencies**:
   
cd Server
pip install -r requirements.txt

3. **Flash ESP32-CAM firmware**:
- Open ESP32 code in Arduino IDE
- Configure board settings
- Upload firmware
  
4. **Program STM32F4**:
- Open STM32 project in STM32CubeIDE
- Build and flash firmware
  
🚀 Usage
1. **Start the server**:
   
python main.py

2. **Access web interface**:
   
http://localhost:5000

3. **Register new users**:
- Click "Sign Up"
- Fill in user information
- Look at the camera when submitting
- Wait for confirmation

4. **Regular usage**:
- Stand in front of the camera
- System automatically recognizes registered users
- Gate opens for authorized personnel
- LED display shows entry status

🎥 Demo
Watch Demo Video

🛠 Technologies Used
- Face Recognition: face_recognition library, OpenCV
- Web Framework: Flask, SocketIO
- Frontend: HTML, JavaScript
- Embedded: STM32 HAL, Arduino
- Communication: USB, WiFi
- Database: JSON
  
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📝 License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/gkynajru/Automated-facial-recognition-entry-management-system/blob/iot_system/LICENSE) for details.
   
