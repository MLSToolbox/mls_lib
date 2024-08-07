from mls_lib.data_cleaning import DataCleaningStep
from mls_lib.objects import Object

class ReplaceNull(DataCleaningStep):
    def __init__(self, strategy : str, column : str, data_in : Object):
        super().__init__(
            data_in = data_in
        )
        
        self.column = column
        self.strategy = strategy

    def execute(self):
        data = self._getInput("data_in").copy()

        df = data.getData()
        
        if self.strategy == 'average':
            self.__useAvg(df)
        elif self.strategy == 'zero':
            self.__useZero(df)
        elif self.strategy == 'mode':
            self.__useMode(df)

        data.setData(df)

        self._setOutput("out", data)

        self.finishExecution()

    def __useAvg(self, df):
        df[self.column] = df[self.column].fillna(df[self.column].mean())
        
    def __useMode(self, df):
        df[self.column] = df[self.column].fillna(df[self.column].mode()[0])        

    def __useZero(self, df):
        df[self.column] = df[self.column].fillna(0)