import pandas as pd
import pytest
import numpy as np

# Assuming mls_lib is accessible in your test environment
from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.data_cleaning import ReplaceValue # Assuming ReplaceValue is in mls_lib.components

class TestReplaceValue:
    """
    Test suite for the ReplaceValue component.
    """

    @pytest.fixture
    def sample_dataframe(self):
        """
        Provides a sample DataFrame for testing, initialized correctly.
        """
        data = {
            'numeric_col': [1, 2, 3, 4, 5],
            'string_col': ['apple', 'banana', 'cherry', 'apple', 'date'],
            'mixed_col': [10, 'twenty', 30, 'forty', 50],
            'other_col': [100, 200, 300, 400, 500]
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
        Tests the initialization of the ReplaceValue component.
        """
        column_name = 'test_col'
        value_map = {'old': 'new'}
        task = ReplaceValue(column=column_name, value_map=value_map)

        assert task.column == column_name
        assert task.value_map == value_map
        assert isinstance(task.data_in, DataFrame)
        assert isinstance(task, Task)

    def test_set_data(self, sample_dataframe):
        """
        Tests the set_data method.
        """
        task = ReplaceValue(column='numeric_col', value_map={1: 10})
        task.set_data(sample_dataframe)
        pd.testing.assert_frame_equal(task.data_in.get_data(), sample_dataframe.get_data())

    def test_execute_basic_replacement_numeric(self, sample_dataframe):
        """
        Tests basic replacement of numeric values.
        """
        column_to_replace = 'numeric_col'
        value_map = {1: 100, 3: 300, 5: 500}
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        task.execute()

        result_df_obj = task.get_output("out")
        # Values not in map (2, 4) should become NaN
        expected_series = pd.Series([100, np.nan, 300, np.nan, 500], name=column_to_replace)
        pd.testing.assert_series_equal(result_df_obj.get_data()[column_to_replace], expected_series, check_dtype=False)
        # Check that other columns are unchanged
        pd.testing.assert_series_equal(result_df_obj.get_data()['other_col'], sample_dataframe.get_data()['other_col'], check_dtype=False)


    def test_execute_basic_replacement_string(self, sample_dataframe):
        """
        Tests basic replacement of string values.
        """
        column_to_replace = 'string_col'
        value_map = {'apple': 'red_apple', 'banana': 'yellow_banana'}
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        task.execute()

        result_df_obj = task.get_output("out")
        # 'cherry', 'date' not in map should become NaN
        expected_series = pd.Series(['red_apple', 'yellow_banana', np.nan, 'red_apple', np.nan],
                                    name=column_to_replace, dtype='object')
        pd.testing.assert_series_equal(result_df_obj.get_data()[column_to_replace], expected_series)

    def test_execute_replacement_with_different_datatypes(self, sample_dataframe):
        """
        Tests replacing values with different data types (e.g., number to string, string to number).
        """
        column_to_replace = 'mixed_col'
        # Replace 10 (int) with 'ten' (str), 'twenty' (str) with 20 (int)
        value_map = {10: 'ten', 'twenty': 20, 30: 30.0}
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        task.execute()

        result_df_obj = task.get_output("out")
        # 'forty', 50 not in map should become NaN
        expected_series = pd.Series(['ten', 20, 30.0, np.nan, np.nan], name=column_to_replace, dtype='object')
        pd.testing.assert_series_equal(result_df_obj.get_data()[column_to_replace], expected_series)


    def test_execute_values_not_in_map_become_nan(self, sample_dataframe):
        """
        Tests that values not explicitly in the value_map are converted to NaN.
        """
        column_to_replace = 'numeric_col'
        value_map = {1: 10} # Only map value 1
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        task.execute()

        result_df_obj = task.get_output("out")
        expected_series = pd.Series([10, np.nan, np.nan, np.nan, np.nan], name=column_to_replace)
        pd.testing.assert_series_equal(result_df_obj.get_data()[column_to_replace], expected_series)

    def test_execute_empty_value_map(self, sample_dataframe):
        """
        Tests behavior when the value_map is empty. All values should become NaN.
        """
        column_to_replace = 'numeric_col'
        value_map = {} # Empty map
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        task.execute()

        result_df_obj = task.get_output("out")
        expected_series = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan], name=column_to_replace, dtype=float)
        pd.testing.assert_series_equal(result_df_obj.get_data()[column_to_replace], expected_series)

    def test_execute_non_existent_column(self, sample_dataframe):
        """
        Tests that a KeyError is raised if the specified column does not exist.
        """
        column_to_replace = 'non_existent_col'
        value_map = {'a': 'b'}
        task = ReplaceValue(column=column_to_replace, value_map=value_map)
        task.set_data(sample_dataframe)

        with pytest.raises(KeyError, match=f"'{column_to_replace}'"):
            task.execute()

    def test_output_is_set(self, sample_dataframe):
        """
        Ensures the output is correctly set and is a DataFrame object.
        """
        task = ReplaceValue(column='numeric_col', value_map={1: 10})
        task.set_data(sample_dataframe)
        task.execute()

        output_df_obj = task.get_output("out")
        assert isinstance(output_df_obj, DataFrame)