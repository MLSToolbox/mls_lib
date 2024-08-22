""" StandardScalerTrainer: Component that trains a standard scaler. """

from mls_lib.objects.scalers import StandardScaler as SS
from mls_lib.objects.data_frame import DataFrame

from . scaler_trainer import ScalerTrainer

class StandardScalerTrainer(ScalerTrainer):
    """ StandardScalerTrainer: Component that trains a standard scaler. """
    def __init__(self, columns : list, data : DataFrame):
        super().__init__(
            columns = columns,
            data = data,
            scaler = SS()
        )
    