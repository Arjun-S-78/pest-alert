
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_pest(img_path):
    results = model(img_path)
    for r in results:
        if len(r.boxes) > 0:
            pest = r.names[int(r.boxes.cls[0])]
            conf = float(r.boxes.conf[0])
            return pest, round(conf, 2)
    return "No Pest", 0.0
