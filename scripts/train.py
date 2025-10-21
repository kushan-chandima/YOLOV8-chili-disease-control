from ultralytics import YOLO
import yaml
import os
from pathlib import Path

# Define paths
base_path = Path("ai-yolov8-chili-disease-control")  # repo folder
data_path = base_path / "dataset"
config_path = data_path / "data.yaml"
model_save_path = base_path / "runs" / "train"

# Create directories if they don't exist
os.makedirs(data_path, exist_ok=True)
os.makedirs(model_save_path, exist_ok=True)

# Define dataset configuration
config = {
    "path": str(data_path),
    "train": "images",
    "val": "valid",
    "task": "detect",
    "nc": 1,
    "names": ["Disease"],
}

# Save YAML config
with open(config_path, 'w') as file:
    yaml.dump(config, file)

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")

# Train the model
model.train(
    data=str(config_path),
    epochs=150,
    imgsz=640,
    project=str(model_save_path),
    name="exp"
)
