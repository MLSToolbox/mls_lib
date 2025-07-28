""" YOLOv11Trainer: Component that trains and makes image predictions. """

from mls_lib.orchestration.task import Task
from mls_lib.objects.models.yolov11_model import YOLOv11Model
from mls_lib.objects.data_frame import DataFrame
class YOLOv11Trainer(Task):
    """ YOLOv11Trainer: Component that trains and makes image predictions. """
    def __init__(self, data_path: str, epochs: int, imgsz: int) -> None:
        super().__init__()
        self.mlslib_model = YOLOv11Model()
        self.train_result = DataFrame()
        self.data_path = data_path
        self.epochs = epochs
        self.imgsz = imgsz

    def execute(self):
        result = self.mlslib_model.train(
            data_path = self.data_path,
            epochs = self.epochs,
            imgsz = self.imgsz
        )

        self.train_result.set_data(result)

        print("Model trained, it was saved in path:", self.mlslib_model.trained_model_path)

        self._set_output("model", self.mlslib_model)
        self._set_output("train_stats", self.train_result)
