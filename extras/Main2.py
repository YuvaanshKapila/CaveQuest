from ultralytics import YOLO

model = YOLO("best.pt")

model.predict("Leaf pic.jpg", save=True, show=True, conf=0.1)