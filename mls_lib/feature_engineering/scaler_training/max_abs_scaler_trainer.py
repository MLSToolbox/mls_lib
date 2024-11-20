""" MaxAbsScalerTrainer: Component that trains a max abs scaler. """

from mls_lib.objects.scalers import MaxAbsScaler as MAS

from .scaler_trainer import ScalerTrainer

class MaxAbsScalerTrainer(ScalerTrainer):
    """ MaxAbsScalerTrainer: Component that trains a max abs scaler. """
    def __init__(self, columns : list):
        super().__init__(columns)
        self.scaler = MAS()
