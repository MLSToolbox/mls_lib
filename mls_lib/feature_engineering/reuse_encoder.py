""" Reuse Encoder """

from mls_lib.orchestration.task import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.encoders.iencoder import IEncoder

class ReuseEncoder(Task):
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

        data = self.encoder.transform(df)
        
        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("out", new_df)
