import pandas as pd
import pytest

from mls_lib.objects.data_frame import DataFrame
from mls_lib.orchestration.task import Task
from mls_lib.feature_engineering import DuplicateColumn

class TestDuplicateColumn:
    """
    Test suite for the DuplicateColumn component.
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
        Tests the initialization of the DuplicateColumn component.
        """
        original_col = 'col_a'
        new_col = 'col_a_copy'
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)

        assert duplicate_column_task.original_column_name == original_col
        assert duplicate_column_task.new_column_name == new_col
        assert isinstance(duplicate_column_task.old_table, DataFrame)
        assert isinstance(duplicate_column_task, Task)

    def test_set_data(self, sample_dataframe):
        """
        Tests the set_data method of the DuplicateColumn component.
        """
        original_col = 'col_a'
        new_col = 'col_a_copy'
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)
        duplicate_column_task.set_data(sample_dataframe)

        pd.testing.assert_frame_equal(duplicate_column_task.old_table.get_data(), sample_dataframe.get_data())

    def test_execute_successful_duplication(self, sample_dataframe):
        """
        Tests the execute method for successful column duplication.
        """
        original_col = 'col_a'
        new_col = 'col_a_copy'
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)
        duplicate_column_task.set_data(sample_dataframe)
        duplicate_column_task.execute()

        expected_data = pd.DataFrame({
            'col_a': [1, 2, 3],
            'col_b': [4, 5, 6],
            'col_c': [7, 8, 9],
            'col_a_copy': [1, 2, 3] # The duplicated column
        })

        output_df = duplicate_column_task.get_output("new_table").get_data()
        pd.testing.assert_frame_equal(output_df, expected_data)
        assert new_col in output_df.columns
        pd.testing.assert_series_equal(output_df[original_col], output_df[new_col], check_names=False)


    def test_execute_duplicate_to_existing_column(self, sample_dataframe):
        """
        Tests that duplicating a column to an existing column name overwrites it.
        """
        original_col = 'col_a'
        new_col = 'col_b' # Overwriting an existing column
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)
        duplicate_column_task.set_data(sample_dataframe)
        duplicate_column_task.execute()

        expected_data = pd.DataFrame({
            'col_a': [1, 2, 3],
            'col_b': [1, 2, 3], # col_b should now have col_a's data
            'col_c': [7, 8, 9]
        })

        output_df = duplicate_column_task.get_output("new_table").get_data()
        pd.testing.assert_frame_equal(output_df, expected_data)
        pd.testing.assert_series_equal(output_df[original_col], output_df[new_col], check_names=False)

    def test_execute_original_column_not_found(self, sample_dataframe):
        """
        Tests that a KeyError is raised if the original column does not exist.
        """
        original_col = 'non_existent_col'
        new_col = 'new_col'
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)
        duplicate_column_task.set_data(sample_dataframe)

        with pytest.raises(KeyError):
            duplicate_column_task.execute()

    def test_output_name_is_new_table(self, sample_dataframe):
        """
        Ensures the output DataFrame is stored under the key "new_table".
        """
        original_col = 'col_a'
        new_col = 'col_a_copy'
        duplicate_column_task = DuplicateColumn(original_column_name=original_col, new_column_name=new_col)
        duplicate_column_task.set_data(sample_dataframe)
        duplicate_column_task.execute()

        assert isinstance(duplicate_column_task.get_output("new_table"), DataFrame)