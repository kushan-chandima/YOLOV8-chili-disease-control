from ultralytics import YOLO
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import serial
import time

class YOLODetector:
    def __init__(self, model_path, confidence_threshold=0.6):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.color_map = {
            0: (255, 0, 0),  # Class 0 - Red
            1: (0, 255, 0),  # Class 1 - Green
        }
        self.image = None
        self.image_all_boxes = None
        self.image_top_box = None
        self.centers = []
        self.mean_center = None
        self.best_box = None  # Most confident bounding box

    def load_image(self, image_path):
        self.image = cv.imread(image_path)
        if self.image is None:
            raise ValueError("Error: Failed to load image. Check the file path.")
        self.image_all_boxes = self.image.copy()
        self.image_top_box = self.image.copy()

    def detect_objects(self):
        predictions = self.model.predict(self.image, verbose=False)  # Run detection

        best_score = 0  # Track highest confidence score

        for result in predictions:
            h, w = self.image.shape[:2]  # Get image dimensions

            for cls, score, box in zip(
                result.boxes.cls.cpu().numpy(),
                result.boxes.conf.cpu().numpy(),
                result.boxes.xyxy.cpu().numpy()
            ):
                if score < self.confidence_threshold:
                    continue  # Skip detections below threshold

                x1, y1, x2, y2 = box.astype(int)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                self.centers.append((cx, cy))

                class_name = result.names.get(int(cls), f"Class {int(cls)}")

                # Draw bounding box on all-boxes image
                cv.rectangle(self.image_all_boxes, (x1, y1), (x2, y2),
                             self.color_map.get(int(cls), (0, 255, 255)), 2)

                # Draw object center
                cv.circle(self.image_all_boxes, (cx, cy), 5, (0, 0, 255), -1)

                # Display label with confidence score
                label = f"{class_name} {score:.2f}"
                cv.putText(self.image_all_boxes, label, (x1, y1 - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                if score > best_score:
                    best_score = score
                    self.best_box = (x1, y1, x2, y2, cx, cy)

        # Compute mean center if valid objects are detected
        if self.centers:
            mean_cx = int(np.mean([c[0] for c in self.centers]))
            mean_cy = int(np.mean([c[1] for c in self.centers]))
            self.mean_center = (mean_cx, mean_cy)

            # Draw mean center
            cv.circle(self.image_all_boxes, (mean_cx, mean_cy), 7, (0, 255, 255), -1)
            print(f"Mean Center Coordinate: ({mean_cx}, {mean_cy})")

        # Draw only the highest confidence box
        if self.best_box:
            x1, y1, x2, y2, best_cx, best_cy = self.best_box
            cv.rectangle(self.image_top_box, (x1, y1), (x2, y2), (0, 255, 255), 2)  # Yellow box
            cv.circle(self.image_top_box, (best_cx, best_cy), 5, (0, 0, 255), -1)  # Red center

    def determine_area(self):
        """Determines the quadrant of the detected object(s)."""
        if not self.mean_center:
            return []  # Return empty list if no valid detections

        mean_cx, mean_cy = self.mean_center

        if mean_cx < 180 and mean_cy < 320:
            return [1]
        elif mean_cx > 180 and mean_cy < 320:
            return [2]
        elif mean_cx < 180 and mean_cy > 320:
            return [3]
        else:
            return [4]

    def display_image(self, image_type="original", auto_close_delay=0):
        if image_type == "original":
            img = self.image
        elif image_type == "all_boxes":
            img = self.image_all_boxes
        elif image_type == "top_box":
            img = self.image_top_box
        else:
            raise ValueError("Invalid image type! Choose 'original', 'all_boxes', or 'top_box'.")

        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show(block=False)  # Show the image without blocking
        
        if auto_close_delay > 0:
            plt.pause(auto_close_delay)  # Pause for the specified delay
            plt.close()  # Close the current plot
        
        
    def send_to_esp32(self, area):
        try:
            ser = serial.Serial('COM3', 115200, timeout=2)
            time.sleep(2)
            command = str(area[0])
            ser.write(command.encode())
            print(f"Sent to ESP32: {command}")
            ser.close()
        except Exception as e:
            print("Error communicating with ESP32:", e)


# === MAIN EXECUTION === #
if __name__ == "__main__":
    model_path = r'runs/detect/train/weights/best.pt'
    image_path = r'data/test/PXL_20250129_062431095_MP_jpg.rf.efad41b1b21162560bfbf43c8eb73c8a.jpg'

    detector = YOLODetector(model_path, confidence_threshold=0.6)

    # Load image
    detector.load_image(image_path)

    # Display original image
    print("Displaying Original Image:")
    #detector.display_image(image_type="original", auto_close_delay=3)
    
    # Run object detection
    detector.detect_objects()

    # Display image with all bounding boxes
    print("Displaying Image with All Bounding Boxes:")
    detector.display_image(image_type="all_boxes", auto_close_delay=3)

    # Display image with only the highest confidence bounding box
    print("Displaying Image with Most Confident Bounding Box:")
    #detector.display_image(image_type="top_box")

    # Determine the area of detected object(s)
    area = detector.determine_area()

    # Print area as a list
    print("Determined Area:", area)
    
    detector.send_to_esp32(area)
