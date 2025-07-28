import pandas as pd
import pytest
import numpy as np

from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.data_cleaning import ReplaceNullMode

class TestReplaceNullMode:
    """
    Test suite for the ReplaceNullMode component.
    """

    @pytest.fixture
    def sample_dataframe_with_nulls(self):
        """
        Provides a sample DataFrame with null values for testing, initialized correctly.
        Mode of 'numeric_col' is 2.0 (appears twice).
        Mode of 'categorical_col' is 'apple' (appears twice).
        """
        data = {
            'numeric_col': [1.0, 2.0, np.nan, 2.0, 5.0],
            'categorical_col': ['apple', 'banana', np.nan, 'apple', 'orange'],
            'no_null_col': [100, 200, 300, 400, 500]
        }
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame(data))
        return df_obj

    @pytest.fixture
    def sample_dataframe_no_nulls(self):
        """
        Provides a sample DataFrame with no null values, initialized correctly.
        """
        data = {
            'numeric_col': [1.0, 2.0, 3.0, 4.0, 5.0],
            'categorical_col': ['A', 'B', 'C', 'D', 'E']
        }
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame(data))
        return df_obj

    @pytest.fixture
    def sample_dataframe_all_nulls(self):
        """
        Provides a sample DataFrame where the target column is all nulls, initialized correctly.
        """
        data = {
            'all_null_col': [np.nan, np.nan, np.nan],
            'other_col': [1, 2, 3]
        }
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame(data))
        return df_obj

    @pytest.fixture
    def sample_dataframe_multiple_modes(self):
        """
        Provides a DataFrame with a column having multiple modes (e.g., 1 and 2 both appear twice).
        """
        data = {
            'multi_mode_col': [1, 1, 2, 2, np.nan, 3],
            'other_col': ['X', 'Y', 'Z', 'A', 'B', 'C']
        }
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame(data))
        return df_obj

    @pytest.fixture
    def empty_dataframe(self):
        """
        Provides an empty DataFrame, initialized correctly.
        """
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame())
        return df_obj

    def test_initialization(self):
        """
        Tests the initialization of the ReplaceNullMode component.
        """
        column_name = 'test_col'
        task = ReplaceNullMode(column=column_name)

        assert task.column == column_name
        assert isinstance(task.data_in, DataFrame)
        assert isinstance(task, Task)

    def test_set_data(self, sample_dataframe_with_nulls):
        """
        Tests the set_data method.
        """
        task = ReplaceNullMode(column='numeric_col')
        task.set_data(sample_dataframe_with_nulls)
        pd.testing.assert_frame_equal(task.data_in.get_data(), sample_dataframe_with_nulls.get_data())

    @pytest.mark.parametrize("column_name, expected_mode", [
        ('numeric_col', 2.0),
        ('categorical_col', 'apple')
    ])
    def test_execute_replaces_nulls_with_mode(self, sample_dataframe_with_nulls, column_name, expected_mode):
        """
        Tests that null values are correctly replaced by the column's mode.
        """
        task = ReplaceNullMode(column=column_name)
        task.set_data(sample_dataframe_with_nulls)

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_name]

        # Check if nulls are replaced
        assert not result_series.isnull().any()

        # Check the values where nulls were
        original_data = sample_dataframe_with_nulls.get_data()
        for i, val in original_data[column_name].items():
            if pd.isna(val):
                assert result_series.iloc[i] == expected_mode
            else:
                assert result_series.iloc[i] == val

    def test_execute_column_with_no_nulls_remains_unchanged(self, sample_dataframe_no_nulls):
        """
        Tests that a column with no null values remains unchanged.
        """
        column_to_impute = 'numeric_col'
        task = ReplaceNullMode(column=column_to_impute)
        task.set_data(sample_dataframe_no_nulls)

        original_data = sample_dataframe_no_nulls.get_data().copy()

        task.execute()

        result_df_obj = task.get_output("out")
        pd.testing.assert_frame_equal(result_df_obj.get_data(), original_data)

    def test_execute_column_all_nulls_raises_error(self, sample_dataframe_all_nulls):
        """
        Tests that accessing mode()[0] on an all-null column raises an IndexError.
        This is the expected behavior based on the current implementation.
        """
        column_to_impute = 'all_null_col'
        task = ReplaceNullMode(column=column_to_impute)
        task.set_data(sample_dataframe_all_nulls)

        with pytest.raises(KeyError):
            task.execute()

    def test_execute_column_multiple_modes(self, sample_dataframe_multiple_modes):
        """
        Tests behavior when the target column has multiple modes.
        The implementation `mode()[0]` will pick the first mode found.
        """
        column_to_impute = 'multi_mode_col'
        task = ReplaceNullMode(column=column_to_impute)
        task.set_data(sample_dataframe_multiple_modes)

        # The modes are [1, 2]. mode()[0] will pick 1.
        expected_mode = 1

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_to_impute]

        assert not result_series.isnull().any()
        expected_series = pd.Series([1, 1, 2, 2, expected_mode, 3], name=column_to_impute)
        pd.testing.assert_series_equal(result_series, expected_series, check_dtype=False)

    def test_execute_non_existent_column(self, sample_dataframe_with_nulls):
        """
        Tests that a KeyError is raised if the specified column does not exist.
        """
        column_to_impute = 'non_existent_col'
        task = ReplaceNullMode(column=column_to_impute)
        task.set_data(sample_dataframe_with_nulls)

        with pytest.raises(KeyError, match=f"'{column_to_impute}'"):
            task.execute()

    def test_output_is_set(self, sample_dataframe_no_nulls):
        """
        Ensures the output is correctly set and is a DataFrame object.
        """
        task = ReplaceNullMode(column='numeric_col')
        task.set_data(sample_dataframe_no_nulls)
        task.execute()

        output_df_obj = task.get_output("out")
        assert isinstance(output_df_obj, DataFrame)