""" MaxAbsScalerTrainer: Component that trains a max abs scaler. """

from mls_lib.objects.scalers import MaxAbsScaler as MAS
from mls_lib.orchestration.step import Step

from . scaler_trainer import ScalerTrainer

class MaxAbsScalerTrainer(ScalerTrainer):
    """ MaxAbsScalerTrainer: Component that trains a max abs scaler. """
    def __init__(self, columns : list, data : Step):
        super().__init__(
            columns = columns,
            data = data
        )

        self.scaler = MAS()
    