from . data_transformer import DataTransformer

class Join(DataTransformer):
    def __init__(self, left, right, on, how):
        super().__init__(
            left = left,
            right = right,
        )
        self.on = on
        self.how = how

    def execute(self): # FIXME: write functionality
        pass