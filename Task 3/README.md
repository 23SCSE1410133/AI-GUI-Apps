# Task 3 - 🧠 Real-Time Object Detection & Tracking App

A Python desktop application for **real-time object detection and tracking** using the **YOLOv5u model** and **Deep SORT algorithm**, integrated with a clean **Tkinter GUI** for ease of use.

---
## 🎯 Features

- 📹 **Real-time object detection** via YOLOv5u  
- 🔁 **Multi-object tracking** using Deep SORT  
- 🧠 Identity assignment for each tracked object (ID labels)  
- 🖼️ Live video stream display on a GUI (via webcam or uploaded video)  
- 📁 Easy file loading via button (`.mp4`, `.avi`, `.mov`, `.mkv`)  
- 🛑 Start/Stop buttons for full control  

---
## 🛠️ Technologies Used

- [`ultralytics`](https://github.com/ultralytics/ultralytics) (YOLOv5u detection model)
- [`deep_sort_realtime`](https://pypi.org/project/deep-sort-realtime/) (tracking)
- [`opencv-python`](https://pypi.org/project/opencv-python/)
- [`Pillow`](https://pypi.org/project/Pillow/) (image rendering)
- Built-in `Tkinter` GUI

---
## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Install required dependencies**
   ```bash
   pip install ultralytics deep_sort_realtime opencv-python Pillow

3. **Run the app**
   ```bash
   python ObjID_app.py
---
## 🧪 How It Works

- The app loads a video file or activates your webcam.
- Each frame is passed through the YOLOv5u model for object detection.
- Detected objects are passed to the Deep SORT tracker, which assigns unique IDs and tracks them over time.
- The result is drawn live onto a GUI canvas using Tkinter and Pillow.
---
## ✨Made by Anushka Sharma✨
