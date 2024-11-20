""" RobustScalerTrainer: Component that trains a robust scaler. """

from mls_lib.objects.scalers import RobustScaler as RS

from . scaler_trainer import ScalerTrainer

class RobustScalerTrainer(ScalerTrainer):
    """ RobustScalerTrainer: Component that trains a robust scaler. """
    def __init__(self, columns : list):
        super().__init__(columns)

        self.scaler = RS()
