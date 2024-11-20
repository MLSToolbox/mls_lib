""" MinMaxScalerTrainer: Component that trains a min max scaler. """

from mls_lib.objects.scalers import MinMaxScaler as MMS

from . scaler_trainer import ScalerTrainer

class MinMaxScalerTrainer(ScalerTrainer):
    """ MinMaxScalerTrainer: Component that trains a min max scaler. """
    def __init__(self, columns : list):
        super().__init__(columns)
        self.scaler = MMS()
