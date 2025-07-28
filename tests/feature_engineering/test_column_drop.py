import pandas as pd
import pytest

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.feature_engineering import ColumnDrop

class TestColumnDrop:
    """
    Test suite for the ColumnDrop component.
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
        Tests the initialization of the ColumnDrop component.
        """
        columns_to_drop = ['col_a', 'col_c']
        column_drop_task = ColumnDrop(columns=columns_to_drop)

        assert column_drop_task.columns == columns_to_drop
        assert isinstance(column_drop_task.origin_table, DataFrame)
        assert isinstance(column_drop_task.resulting_table, DataFrame)
        assert isinstance(column_drop_task, Task)

    def test_set_data(self, sample_dataframe):
        """
        Tests the set_data method of the ColumnDrop component.
        """
        columns_to_drop = ['col_a']
        column_drop_task = ColumnDrop(columns=columns_to_drop)
        column_drop_task.set_data(sample_dataframe)

        pd.testing.assert_frame_equal(column_drop_task.origin_table.get_data(), sample_dataframe.get_data())

    def test_execute_single_column_drop(self, sample_dataframe):
        """
        Tests the execute method for dropping a single column.
        """
        columns_to_drop = ['col_a']
        column_drop_task = ColumnDrop(columns=columns_to_drop)
        column_drop_task.set_data(sample_dataframe)
        column_drop_task.execute()

        expected_data = pd.DataFrame({'col_b': [4, 5, 6], 'col_c': [7, 8, 9]})
        pd.testing.assert_frame_equal(column_drop_task.resulting_table.get_data(), expected_data)
        pd.testing.assert_frame_equal(column_drop_task.get_output("resulting_table").get_data(), expected_data)

    def test_execute_multiple_columns_drop(self, sample_dataframe):
        """
        Tests the execute method for dropping multiple columns.
        """
        columns_to_drop = ['col_a', 'col_c']
        column_drop_task = ColumnDrop(columns=columns_to_drop)
        column_drop_task.set_data(sample_dataframe)
        column_drop_task.execute()