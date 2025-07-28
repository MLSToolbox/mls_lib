""" LinearRegressionModel: Component that trains and makes predictions. """
from . model import Model
from ultralytics import YOLO
import os

class YOLOv11Model(Model):
    """ LinearRegressionModel: Component that trains and makes predictions. """
    def __init__(self, model_name: str):
        super().__init__()
        self.model = YOLO(model_name)
        self.trained_model_path = ""

    def train(self, data_path: str, epochs = 5, imgsz = 640):
        """ Train the model. """
        results = self.model.train(data = data_path, epochs = epochs, imgsz = imgsz, save = False)
        self.trained_model_path = os.path.join(results["save_dir"],"best.pt")
        self.metrics = results["results_dict"]

        self.model = YOLO(self.trained_model_path)

    def predict(self, image_paths: list, save_folder: str):
        """ Predict the labels for the given image paths using the model. """
        results = self.model(image_paths)

        for i, result in enumerate(results):
            result.save(filename=os.join(save_folder, "predicted_" + os.path.basename(image_paths[i])))