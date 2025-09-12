""" Pickle Loader """
import pandas as pd
import numpy as np
from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class PickleLoader(Task):
    """ Pickle Loader """
    def __init__(self, path : str):
        super().__init__()
        self.path = path

    def execute(self):
        df = DataFrame()
        pickle = pd.read_pickle(self.path)
        refined_pickle = {}
        for key in pickle.keys():
            if type(pickle[key]) == pd.DataFrame:
                refined_pickle[key] = pickle[key]
            elif type(pickle[key]) == list:
                refined_pickle[key] = pickle[key]
            elif type(pickle[key]) == np.ndarray:
                refined_pickle[key] = [i for i in pickle[key]]
        data = pd.DataFrame().from_dict(refined_pickle) 
        df.set_data(data)
        self._set_output("out", df)
