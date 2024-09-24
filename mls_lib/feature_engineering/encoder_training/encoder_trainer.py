""" Encoder Trainer """

from mls_lib.orchestration.step import Step
from mls_lib.objects.encoders.encoder import IEncoder
from mls_lib.objects.data_frame import DataFrame

class EncoderTrainer(Step):
    """ Encoder Trainer """
    def __init__(self, columns : list) -> None:
        super().__init__()
        self.columns = columns
        self.data = DataFrame()
        self.encoder = IEncoder()
    
    def set_data(self, columns : list, data : DataFrame) -> None:
        self.columns = columns
        self.data = data

    def execute(self):
        df = self.data.get_data()

        self.encoder.fit_transform(df, self.columns)

        self.data.set_data(df)

        self._set_output("encoder", self.encoder)

        self._set_output("out", self.data)
