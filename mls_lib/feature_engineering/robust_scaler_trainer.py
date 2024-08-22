""" RobustScalerTrainer: Component that trains a robust scaler. """

from mls_lib.objects.scalers import RobustScaler as RS
from mls_lib.objects.data_frame import DataFrame

from . scaler_trainer import ScalerTrainer

class RobustScalerTrainer(ScalerTrainer):
    """ RobustScalerTrainer: Component that trains a robust scaler. """
    def __init__(self, columns : list, data : DataFrame):
        super().__init__(
            columns = columns,
            data = data,
            scaler = RS()
        )
    