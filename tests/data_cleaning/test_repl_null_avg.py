import pandas as pd
import pytest
import numpy as np

from mls_lib.orchestration import Task
from mls_lib.objects.data_frame import DataFrame
from mls_lib.data_cleaning import ReplaceNullAverage

class TestReplaceNullAverage:
    """
    Test suite for the ReplaceNullAverage component.
    """

    @pytest.fixture
    def sample_dataframe_with_nulls(self):
        """
        Provides a sample DataFrame with null values for testing, initialized correctly.
        """
        data = {
            'numeric_col': [1.0, 2.0, np.nan, 4.0, 5.0],
            'another_col': [10, np.nan, 30, 40, 50],
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
            'another_col': [10, 20, 30, 40, 50]
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
    def empty_dataframe(self):
        """
        Provides an empty DataFrame, initialized correctly.
        """
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame())
        return df_obj

    @pytest.fixture
    def dataframe_with_non_numeric_col(self):
        """
        Provides a DataFrame with a non-numeric column, initialized correctly.
        """
        data = {
            'string_col': ['a', np.nan, 'c'],
            'numeric_col': [1, 2, 3]
        }
        df_obj = DataFrame()
        df_obj.set_data(pd.DataFrame(data))
        return df_obj


    def test_initialization(self):
        """
        Tests the initialization of the ReplaceNullAverage component.
        """
        column_name = 'test_col'
        task = ReplaceNullAverage(column=column_name)

        assert task.column == column_name
        assert isinstance(task.data_in, DataFrame)
        assert isinstance(task, Task)

    def test_set_data(self, sample_dataframe_with_nulls):
        """
        Tests the set_data method.
        """
        task = ReplaceNullAverage(column='numeric_col')
        task.set_data(sample_dataframe_with_nulls)
        pd.testing.assert_frame_equal(task.data_in.get_data(), sample_dataframe_with_nulls.get_data())

    def test_execute_replaces_nulls_with_average(self, sample_dataframe_with_nulls):
        """
        Tests that null values are correctly replaced by the column's mean.
        """
        column_to_impute = 'numeric_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(sample_dataframe_with_nulls)

        # Calculate expected mean manually
        original_data = sample_dataframe_with_nulls.get_data()
        mean_value = original_data[column_to_impute].mean() # (1.0 + 2.0 + 4.0 + 5.0) / 4 = 12.0 / 4 = 3.0

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_to_impute]

        # Check if nulls are replaced
        assert not result_series.isnull().any()

        # Check the values
        expected_series = pd.Series([1.0, 2.0, mean_value, 4.0, 5.0], name=column_to_impute)
        pd.testing.assert_series_equal(result_series, expected_series)

    def test_execute_column_with_no_nulls_remains_unchanged(self, sample_dataframe_no_nulls):
        """
        Tests that a column with no null values remains unchanged.
        """
        column_to_impute = 'numeric_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(sample_dataframe_no_nulls)

        original_data = sample_dataframe_no_nulls.get_data().copy() # Make a copy to compare

        task.execute()

        result_df_obj = task.get_output("out")
        pd.testing.assert_frame_equal(result_df_obj.get_data(), original_data)

    def test_execute_column_all_nulls(self, sample_dataframe_all_nulls):
        """
        Tests behavior when the target column contains only null values.
        The mean of an all-NaN series is NaN, so fillna will keep them as NaN.
        """
        column_to_impute = 'all_null_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(sample_dataframe_all_nulls)

        task.execute()

        result_df_obj = task.get_output("out")
        result_series = result_df_obj.get_data()[column_to_impute]

        # All values should still be NaN, as mean of all NaNs is NaN
        assert result_series.isnull().all()
        # Verify other columns are untouched
        pd.testing.assert_series_equal(result_df_obj.get_data()['other_col'],
                                       pd.Series([1, 2, 3], name='other_col'))

    def test_execute_non_existent_column(self, sample_dataframe_with_nulls):
        """
        Tests that a KeyError is raised if the specified column does not exist.
        """
        column_to_impute = 'non_existent_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(sample_dataframe_with_nulls)

        with pytest.raises(KeyError, match=f"'{column_to_impute}'"):
            task.execute()

    def test_execute_empty_dataframe(self, empty_dataframe):
        """
        Tests behavior with an empty input DataFrame.
        Accessing a column from an empty DataFrame will usually create it,
        but `mean()` will result in NaN, and fillna will then effectively do nothing.
        """
        column_to_impute = 'some_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(empty_dataframe)

        with pytest.raises(KeyError):
            task.execute()


    def test_execute_non_numeric_column(self, dataframe_with_non_numeric_col):
        """
        Tests behavior when the target column is non-numeric.
        Pandas `mean()` on a Series with non-numeric data (like strings) will typically return NaN or raise
        a TypeError if it cannot compute the mean. `fillna(NaN)` will then do nothing.
        """
        column_to_impute = 'string_col'
        task = ReplaceNullAverage(column=column_to_impute)
        task.set_data(dataframe_with_non_numeric_col)

        with pytest.raises(TypeError):
            task.execute()


    def test_output_is_set(self, sample_dataframe_no_nulls):
        """
        Ensures the output is correctly set and is a DataFrame object.
        """
        task = ReplaceNullAverage(column='numeric_col')
        task.set_data(sample_dataframe_no_nulls)
        task.execute()

        output_df_obj = task.get_output("out")
        assert isinstance(output_df_obj, DataFrame)