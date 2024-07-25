from .text_loader import TextLoader

class CSVLoader(TextLoader):
    def __init__(self, path):
        super().__init__(path)
        pass

    def load(self):
        pass