from ultralytics import YOLO

model = YOLO("best.pt")

model.predict(0, save=True, show=True, conf=0.1)