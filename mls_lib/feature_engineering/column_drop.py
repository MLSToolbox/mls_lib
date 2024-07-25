from . data_transformer import DataTransformer

class ColumnDrop(DataTransformer):
    def __init__(self, origin, columns):
        super().__init__(
            origin = origin
        )
        
        self.columns = columns
        
    def transform(self):
        origin, port = self.__getInput("origin")
        dataframe = origin.get(port)
        
        data = dataframe.getData()
        data = data.drop(self.columns, axis=1)
        
        dataframe.setData(data)

        self.__setOutput("resulting_table", dataframe)