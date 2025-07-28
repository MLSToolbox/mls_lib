import pandas as pd
import pytest
import numpy as np

from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.data_cleaning import ReplaceNullZero

class TestReplaceNullZero:
    """
    Test suite for the ReplaceNullZero component.
    """

    @pytest.fixture
    def sample_dataframe_with_nulls(self):
        """
        Provides a sample DataFrame with null values for testing, initialized correctly.
        """
        data = {
            'numeric_col': [1, 2, np.nan, 4, 5],
            'float_col': [1.1, np.nan, 3.3, 4.4, np.nan],
            'string_col': ['apple', np.nan, 'banana', 'orange', np.nan],
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
            'numeric_col': [1, 2, 3, 4, 5],
            'float_col': [1.1, 2.2, 3.3, 4.4, 5.5],
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
            'all_null_numeric': [np.nan, np.nan, np.nan],
            'all_null_string': [np.nan, np.nan, np.nan],
            'other_col': [1, 2, 3]
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
        Tests the initialization of the ReplaceNullZero component.
        """
        column_name = 'test_col'
        task = ReplaceNullZero(column=column_name)

        assert task.column == column_name
        assert isinstance(task.data_in, DataFrame)
        assert isinstance(task, Task)

    def test_set_data(self, sample_dataframe_with_nulls):
        """
        Tests the set_data method.
        """
        task = ReplaceNullZero(column='numeric_col')
        task.set_data(sample_dataframe_with_nulls)
        pd.testing.assert_frame_equal(task.data_in.get_data(), sample_dataframe_with_nulls.get_data())

    @pytest.mark.parametrize("column_name, expected_data", [
        ('numeric_col', pd.Series([1.0, 2.0, 0.0, 4.0, 5.0], name='numeric_col')),
        ('float_col', pd.Series([1.1, 0.0, 3.3, 4.4, 0.0], name='float_col')),
        ('string_col', pd.Series(['apple', 0, 'banana', 'orange', 0], name='string_col', dtype='object')),
    ])
    def test_execute_replaces_nulls_with_zero(self, sample_dataframe_with_nulls, column_name, expected_data):
        """
        Tests that null values are correctly replaced by 0 for various column types.
        """
        task = ReplaceNullZero(column=column_name)
        task.set_data(sample_dataframe_with_nulls)

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_name]

        # Check if nulls are replaced
        assert not result_series.isnull().any()

        # Check the values
        pd.testing.assert_series_equal(result_series, expected_data)

    def test_execute_column_with_no_nulls_remains_unchanged(self, sample_dataframe_no_nulls):
        """
        Tests that a column with no null values remains unchanged.
        """
        column_to_impute = 'numeric_col'
        task = ReplaceNullZero(column=column_to_impute)
        task.set_data(sample_dataframe_no_nulls)

        original_data = sample_dataframe_no_nulls.get_data().copy()

        task.execute()

        result_df_obj = task.get_output("out")
        pd.testing.assert_frame_equal(result_df_obj.get_data(), original_data)

    @pytest.mark.parametrize("column_name, expected_data", [
        ('all_null_numeric', pd.Series([0.0, 0.0, 0.0], name='all_null_numeric')),
        ('all_null_string', pd.Series([0, 0, 0], name='all_null_string', dtype='object'))
    ])
    def test_execute_column_all_nulls_replaced_with_zero(self, sample_dataframe_all_nulls, column_name, expected_data):
        """
        Tests that a column containing only null values has all its nulls replaced by 0.
        """
        task = ReplaceNullZero(column=column_name)
        task.set_data(sample_dataframe_all_nulls)

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_name]

        assert not result_series.isnull().any()
        pd.testing.assert_series_equal(result_series, expected_data, check_dtype=False)
        # Verify other columns are untouched
        pd.testing.assert_series_equal(result_df_obj.get_data()['other_col'],
                                       pd.Series([1, 2, 3], name='other_col'), check_dtype=False)


    def test_execute_non_existent_column(self, sample_dataframe_with_nulls):
        """
        Tests that a KeyError is raised if the specified column does not exist.
        """
        column_to_impute = 'non_existent_col'
        task = ReplaceNullZero(column=column_to_impute)
        task.set_data(sample_dataframe_with_nulls)

        with pytest.raises(KeyError, match=f"'{column_to_impute}'"):
            task.execute()


    def test_output_is_set(self, sample_dataframe_no_nulls):
        """
        Ensures the output is correctly set and is a DataFrame object.
        """
        task = ReplaceNullZero(column='numeric_col')
        task.set_data(sample_dataframe_no_nulls)
        task.execute()

        output_df_obj = task.get_output("out")
        assert isinstance(output_df_obj, DataFrame)