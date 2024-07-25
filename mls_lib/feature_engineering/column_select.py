from . data_transformer import DataTransformer

class ColumnSelect(DataTransformer):
    def __init__(self, columns):
        super().__init__()
        self.columns = columns

    def execute(self):
        origin, port = self.__getInput("input_table")
        dataframe = origin.get(port)

        data = dataframe.getData()
        data = data[self.columns]

        dataframe.setData(data)

        self.__setOutput("resulting_table", dataframe)