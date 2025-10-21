# ai-yolov8-chili-disease-control

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange?style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-Microcontroller-green?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

**A smart chili plant disease detection and targeted pesticide spraying system using YOLOv8 and a mini robotic sprayer to reduce chemical usage and improve crop health.**

---

## Overview
This project automates the identification and control of **Leaf Curl disease** in chili plants using a YOLOv8 object detection system and a spraying mechanism. A top-view image is processed to detect infected leaves, and the sprayer applies pesticide only to the affected regions, reducing chemical waste and improving efficiency in small-scale crop fields.

---

## System Architecture
Camera → YOLOv8 Detection → ESP32 Controller → Relay & Stepper Motor → Diaphragm Pump → Targeted Pesticide Spray

---

## Hardware Components
- ESP32
- 12V Diaphragm Pump
- 12V 5A SMPS Power Supply
- HW-028 Rain Sensor
- 28BYJ-48 Stepper Motor + ULN2003 Driver
- XL4015 Buck Converter
- Relay Module
- Camera Module (top-view capture)

---

## Software and Tools
- Python
- OpenCV
- Ultralytics YOLOv8
- Roboflow (dataset preparation)
- Arduino IDE (microcontroller programming)

---

## Dataset and Model
- Custom dataset: **440 field images**
- Model: **YOLOv8** (trained for Leaf Curl detection)

---

## 📊 Model Performance
- ✅ Accuracy: **85.6%**
- ✅ Precision: **87.5%**
- 🎯 mAP50: **75.2%**
- Dataset: 440 real field images
- Outcome: Reliable real-time detection and successful selective spraying in field tests

---

## How to Run
```bash
# Clone
git clone https://github.com/yourusername/ai-yolov8-chili-disease-control.git
cd ai-yolov8-chili-disease-control

# Install dependencies
pip install -r requirements.txt

# Run detection
python detect.py --source path_to_images_or_video
