""" MinMaxScalerTrainer: Component that trains a min max scaler. """

from mls_lib.objects.scalers import MinMaxScaler as MMS
from mls_lib.objects.data_frame import DataFrame

from . scaler_trainer import ScalerTrainer

class MinMaxScalerTrainer(ScalerTrainer):
    """ MinMaxScalerTrainer: Component that trains a min max scaler. """
    def __init__(self, columns : list, data : DataFrame):
        super().__init__(
            columns = columns,
            data = data,
            scaler = MMS()
        )
    