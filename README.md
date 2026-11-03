# 🖐️ Gesture Volume Controller (macOS)

Control your Mac's volume with just your hand: no extra hardware, only a standard webcam.

A contactless volume controller built with **Computer Vision and Python**. It tracks your hand in real time and maps the distance between your thumb and index finger to the system volume.

- 🤏 **Pinch close** → Volume down 🔉
- 🖐️ **Spread apart** → Volume up 🔊

## ✨ Features

- Real-time hand tracking with **21 landmarks** via MediaPipe
- Thumb-to-index fingertip distance mapped to a 0–100% volume level
- Exact system volume control on macOS through AppleScript (`osascript`)
- On-screen volume bar, percentage and FPS counter
- Throttled updates so AppleScript isn't called on every frame

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| OpenCV | Webcam capture, drawing and display |
| MediaPipe | Hand landmark detection |
| NumPy | Mapping distance to volume |
| AppleScript (`osascript`) | Setting macOS system volume |

## 📁 Project Structure

```
gesture-volume/
├── gesture_volume_mac.py     # Main script
├── HandTrackingModule.py     # MediaPipe hand detector helper
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/gesture-volume-controller.git
cd gesture-volume-controller
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python gesture_volume_mac.py
```

Press **`q`** in the preview window to quit.

> On first run, macOS will ask for camera access. If the window is black, go to **System Settings → Privacy & Security → Camera** and allow your terminal or IDE.

## 🧠 How It Works

1. **OpenCV** captures frames from the webcam.
2. **MediaPipe** detects the hand and returns 21 landmarks.
3. The script reads the thumb tip (landmark 4) and index fingertip (landmark 8).
4. It calculates the distance between them with `math.hypot`.
5. `np.interp` maps that distance (about 25–250 px) to a 0–100% volume.
6. `osascript` applies the volume to the system.

## ⚙️ Customization

- **Sensitivity:** change the `[25, 250]` range in `np.interp` to suit your hand size and camera distance.
- **Camera:** change `cv2.VideoCapture(0)` if you have more than one camera.
- **Detection confidence:** adjust `detectionCon` in `handDetector`.

## 🔮 Future Improvements

- Mute gesture (closed fist)
- Brightness control with a second hand
- Windows and Linux support
- Smoothing filter for steadier volume changes

## 📄 License

MIT License. Free to use, modify and share.

---

⭐ If you found this project useful, consider giving it a star!
