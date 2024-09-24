""" StandardScalerTrainer: Component that trains a standard scaler. """

from mls_lib.objects.scalers import StandardScaler as SS

from . scaler_trainer import ScalerTrainer

class StandardScalerTrainer(ScalerTrainer):
    """ StandardScalerTrainer: Component that trains a standard scaler. """
    def __init__(self, columns : list):
        super().__init__(columns)

        self.scaler = SS()
