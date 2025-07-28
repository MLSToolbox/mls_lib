"""YOLOv11Model: Component that trains and makes predictions on images generating bounding boxes"""

from .model import Model
from ultralytics import YOLO
import os


class YOLOv11Model(Model):
    """YOLOv11Model: Component that trains and makes predictions on images generating bounding boxes"""

    def __init__(self, model_name: str):
        super().__init__()
        self.model = YOLO(model_name)
        self.trained_model_path = ""

    def train(self, data_path: str, epochs=5, imgsz=640):
        """Train the model."""
        results = self.model.train(
            data=data_path, epochs=epochs, imgsz=imgsz, save=False
        )
        self.trained_model_path = os.path.join(results.save_dir, "weights", "best.pt")

        self.model = YOLO(self.trained_model_path)
        return results.results_dict

    def predict(self, image_paths: list, save_folder: str):
        """Predict the labels for the given image paths using the model."""
        print("Image paths:", image_paths)
        results = self.model(image_paths)

        for i, result in enumerate(results):
            result.save(
                filename=os.path.join(
                    save_folder, "predicted_" + os.path.basename(image_paths[i])
                )
            )
