""" RobustScalerTrainer: Component that trains a robust scaler. """

from mls_lib.objects.scalers import RobustScaler as RS
from mls_lib.orchestration.step import Step

from . scaler_trainer import ScalerTrainer

class RobustScalerTrainer(ScalerTrainer):
    """ RobustScalerTrainer: Component that trains a robust scaler. """
    def __init__(self, columns : list, data : Step):
        super().__init__(
            columns = columns,
            data = data
        )

        self.scaler = RS()
    