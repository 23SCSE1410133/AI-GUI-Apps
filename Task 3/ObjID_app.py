import cv2
import threading
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv5u model
model = YOLO('yolov5su.pt')  # Improved version

# Initialize Deep SORT Tracker
tracker = DeepSort(max_age=30)

# Global variables
video_stream = None
is_running = False
video_path = None

def start_video():
    global video_stream, is_running, video_path
    is_running = True

    if video_path:
        video_stream = cv2.VideoCapture(video_path)
    else:
        video_stream = cv2.VideoCapture(0)

    def process():
        while is_running:
            ret, frame = video_stream.read()
            if not ret:
                break

            # Resize for speed (optional)
            # frame = cv2.resize(frame, (640, 480))

            # YOLOv5u Detection
            results = model(frame, verbose=False)[0]

            detections = []
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf)
                cls = int(box.cls)
                label = model.names[cls]
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, label))

            # Deep SORT Tracking
            tracks = tracker.update_tracks(detections, frame=frame)
            for track in tracks:
                if not track.is_confirmed():
                    continue
                track_id = track.track_id
                l, t, r, b = map(int, track.to_ltrb())
                cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
                cv2.putText(frame, f'ID: {track_id}', (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Show on GUI
            # Resize frame to fit GUI window (e.g., max 800x600)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            # Resize while maintaining aspect ratio
            max_width, max_height = 800, 600
            img.thumbnail((max_width, max_height))

            imgtk = ImageTk.PhotoImage(img)
            lbl_video.imgtk = imgtk
            lbl_video.configure(image=imgtk)


        if video_stream:
            video_stream.release()

    threading.Thread(target=process, daemon=True).start()

def stop_video():
    global is_running
    is_running = False

def open_file():
    global video_path
    path = filedialog.askopenfilename(title="Select Video File",
                                      filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if path:
        video_path = path
        status_label.config(text=f"Loaded: {path.split('/')[-1]}")
    else:
        status_label.config(text="No file selected, defaulting to webcam.")

# GUI Setup
root = Tk()
root.title("YOLOv5u + Deep SORT Object Tracker")
root.geometry("900x700")

lbl_video = Label(root)
lbl_video.pack()

btn_frame = Frame(root)
btn_frame.pack(pady=10)

btn_open = Button(btn_frame, text="📁 Load Video File", command=open_file, width=18)
btn_open.grid(row=0, column=0, padx=5)

btn_start = Button(btn_frame, text="▶ Start Detection", command=start_video, width=18)
btn_start.grid(row=0, column=1, padx=5)

btn_stop = Button(btn_frame, text="⏹ Stop", command=stop_video, width=10)
btn_stop.grid(row=0, column=2, padx=5)

status_label = Label(root, text="No file selected, using webcam by default.", fg="blue")
status_label.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", lambda: [stop_video(), root.destroy()])
root.mainloop()
