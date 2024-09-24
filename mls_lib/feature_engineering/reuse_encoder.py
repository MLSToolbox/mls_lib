""" Reuse Encoder """

from mls_lib.orchestration.step import Step
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.encoders.iencoder import IEncoder

class ReuseEncoder(Step):
    """ Reuse Encoder """
    def __init__(self) -> None:
        super().__init__()

        self.data = DataFrame()
        self.encoder = IEncoder()
    
    def set_data(self, data : DataFrame, encoder : IEncoder) -> None:
        self.data = data
        self.encoder = encoder

    def execute(self):
        df = self.data.get_data()

        self.encoder.transform(df)

        self.data.set_data(df)

        self._set_output("encoder", self.encoder)

        self._set_output("out", self.data)
