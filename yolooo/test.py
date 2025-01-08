from ultralytics import YOLO

# Load a model

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="coco1289.yaml", epochs=50, device="0", batch=2, workers=2)  # train the model
