from . data_collection_step import DataCollectionStep
class TextLoader(DataCollectionStep):
    def __init__(self, path):
        super().__init__()
        self.path = path
        pass

    def execute(self):
        pass

    def load(self):
        pass