""" Image prediction step. """

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.models.model import Model
class ImagePrediction(Task):
    """ Image prediction step. """
    def __init__(self, save_folder: str) -> None:
        super().__init__()

        self.image_paths = DataFrame()
        self.model = Model()
        self.save_folder = save_folder

    def set_data(self, image_paths : DataFrame, model : Model) -> None:
        """
        Sets the data for image prediction.

        Parameters
        ----------
        image_paths : DataFrame
            The image paths to be predicted.
        model : Model
            The model to be used for prediction.

        Returns
        -------
        None
        """
        self.image_paths = image_paths
        self.model = model

    def execute(self) -> None:
        """
        Execute the task.

        This method predicts the labels for the given image paths using the model.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.model.predict(
            image_paths = self.image_paths.get_data(),
            save_folder=self.save_folder)
        
        print("Images predicted, it was saved in path:", self.save_folder)
