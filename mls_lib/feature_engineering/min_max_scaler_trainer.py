""" MinMaxScalerTrainer: Component that trains a min max scaler. """

from mls_lib.objects.scalers import MinMaxScaler as MMS
from mls_lib.orchestration.step import Step

from . scaler_trainer import ScalerTrainer

class MinMaxScalerTrainer(ScalerTrainer):
    """ MinMaxScalerTrainer: Component that trains a min max scaler. """
    def __init__(self, columns : list, data : Step):
        super().__init__(
            columns = columns,
            data = data
        )

        self.scaler = MMS()
    