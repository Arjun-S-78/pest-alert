# 🌱 Pest Alert Pro

## 🚀 Overview

Pest Alert Pro is an AI-powered real-time pest detection system that uses YOLOv8 and OpenCV to identify pests through a live camera feed. The system also tracks location and provides alerts and analytics through a professional web dashboard.

---

## 🎯 Features

* 🎥 Live camera pest detection (real-time)
* 🧠 AI-based classification using YOLOv8
* 📍 Location tracking (Latitude & Longitude)
* ⚠️ Real-time pest alerts
* 📊 Dashboard with pest analytics
* 🗺️ Map visualization of detected pest locations
* 🖥️ Professional UI with animations

---

## 🛠 Tech Stack

* Python (Flask)
* YOLOv8 (Ultralytics)
* OpenCV
* SQLite
* Tailwind CSS
* JavaScript (Chart.js, Leaflet)

---

## 📁 Project Structure

```
pest-alert-pro/
│
├── app.py
├── inference.py
├── pest_info.json
├── database.db
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│
├── static/
│
└── yolov8n.pt
```

---

## ▶️ How to Run

1. Clone the repository:

```
git clone https://github.com/Arjun-S-78/pest-alert.git
cd pest-alert
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Add model file:
   Place `yolov8n.pt` in the project folder

4. Run the application:

```
python app.py
```

5. Open browser:

```
http://127.0.0.1:5000
```



## 📌 Future Enhancements

* 📱 Mobile App Integration
* 📡 SMS / WhatsApp Alerts
* ☁️ Cloud Deployment
* 🌾 IoT-based Smart Farming System

---

## 👨‍💻 Author

**Arjun S**

---

## ⭐ Acknowledgment

This project uses YOLOv8 by Ultralytics for real-time object detection.
