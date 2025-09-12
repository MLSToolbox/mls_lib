""" BasicOperator: Component that changes the value of each element in a column given a dictionary. """

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task

class BasicOperator(Task):
    """ Map: Component that changes the value of each element in a column given a dictionary. """
    def __init__(self, operator: str, value: float, columns: str) -> None:
        super().__init__()
        self.origin_table = DataFrame()
        self.operator = operator
        self.value = float(value)
        self.columns = columns
    def set_data(self, origin_table : DataFrame) -> None:
        """
        Sets the input table to be used for column selection.

        Parameters:
            input_table (DataFrame): The input table to select columns from.

        Returns:
            None
        """
        self.origin_table = origin_table

    def execute(self) -> None:


        data = self.origin_table.get_data()

        for column in self.columns:
            if self.operator == "+":
                data[column] = data[column].apply(lambda x: x + self.value)
            elif self.operator == "-":
                data[column] = data[column].apply(lambda x: x - self.value)
            elif self.operator == "*":
                data[column] = data[column].apply(lambda x: x * self.value)
            elif self.operator == "/":
                data[column] = data[column].apply(lambda x: x / self.value)

        new_df = DataFrame()
        new_df.set_data(data)

        self._set_output("out", new_df)
