""" Encoder Trainer """

from mls_lib.orchestration.task import Task
from mls_lib.objects.encoders.encoder import IEncoder
from mls_lib.objects.data_frame import DataFrame

class EncoderTrainer(Task):
    """ Encoder Trainer """
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.columns = columns
        self.data = DataFrame()
        self.encoder = IEncoder()
    
    def set_data(self, data : DataFrame) -> None:
        self.data = data

    def execute(self):
        df = self.data.get_data()

        new_data = self.encoder.fit_transform(df, self.columns)

        new_df = DataFrame()
        new_df.set_data(new_data)

        self._set_output("encoder", self.encoder)

        self._set_output("out", new_df)
