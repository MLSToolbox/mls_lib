from mls_lib.data_collection import DataCollectionStep
from mls_lib.objects.data_frame import DataFrame

class LoadDataset(DataCollectionStep):
    def __init__(self, path : str, loader : str):
        super().__init__(),
        termination = path.split(".")[-1]
        self.loader = self.getLoaderFromTermination(termination)
        self.path = path
    def execute(self):
        data = DataFrame(
            loader = self.loader,
            path = self.path 
        )

        self.outputs["resulting_table"] = data