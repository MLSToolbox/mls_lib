import pandas as pd
import pytest

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.feature_engineering import ColumnSelect

class TestColumnSelect:
    """
    Test suite for the ColumnSelect component.
    """

    @pytest.fixture
    def sample_dataframe(self):
        """
        Provides a sample DataFrame for testing.
        """
        data = {
            'col_a': [1, 2, 3],
            'col_b': [4, 5, 6],
            'col_c': [7, 8, 9]
        }
        df = DataFrame()
        df.set_data(pd.DataFrame(data))
        return df

    def test_initialization(self):
        """
        Tests the initialization of the ColumnSelect component.
        """
        columns_to_select = ['col_a', 'col_c']
        column_select_task = ColumnSelect(columns=columns_to_select)

        assert column_select_task.columns == columns_to_select
        assert isinstance(column_select_task.origin_table, DataFrame)
        assert isinstance(column_select_task, Task)

    def test_set_data(self, sample_dataframe):
        """
        Tests the set_data method of the ColumnSelect component.
        """
        columns_to_select = ['col_a']
        column_select_task = ColumnSelect(columns=columns_to_select)
        column_select_task.set_data(sample_dataframe)

        pd.testing.assert_frame_equal(column_select_task.origin_table.get_data(), sample_dataframe.get_data())

    def test_execute_single_column_select(self, sample_dataframe):
        """
        Tests the execute method for selecting a single column.
        """
        columns_to_select = ['col_b']
        column_select_task = ColumnSelect(columns=columns_to_select)
        column_select_task.set_data(sample_dataframe)
        column_select_task.execute()

        expected_data = pd.DataFrame({'col_b': [4, 5, 6]})
        pd.testing.assert_frame_equal(column_select_task.get_output("resulting_table").get_data(), expected_data)

    def test_execute_multiple_columns_select(self, sample_dataframe):
        """
        Tests the execute method for selecting multiple columns.
        """
        columns_to_select = ['col_a', 'col_c']
        column_select_task = ColumnSelect(columns=columns_to_select)
        column_select_task.set_data(sample_dataframe)
        column_select_task.execute()

        expected_data = pd.DataFrame({'col_a': [1, 2, 3], 'col_c': [7, 8, 9]})
        pd.testing.assert_frame_equal(column_select_task.get_output("resulting_table").get_data(), expected_data)

    def test_execute_column_not_found(self, sample_dataframe):
        """
        Tests the execute method when trying to select a non-existent column.
        Pandas DataFrame selection with a list of non-existent columns will raise a KeyError.
        """
        columns_to_select = ['non_existent_col']
        column_select_task = ColumnSelect(columns=columns_to_select)
        column_select_task.set_data(sample_dataframe)

        with pytest.raises(KeyError):
            column_select_task.execute()

    def test_execute_select_all_columns(self, sample_dataframe):
        """
        Tests selecting all columns from the DataFrame.
        The resulting DataFrame should be identical to the original.
        """
        columns_to_select = ['col_a', 'col_b', 'col_c']
        column_select_task = ColumnSelect(columns=columns_to_select)
        column_select_task.set_data(sample_dataframe)
        column_select_task.execute()

        pd.testing.assert_frame_equal(column_select_task.get_output("resulting_table").get_data(), sample_dataframe.get_data())