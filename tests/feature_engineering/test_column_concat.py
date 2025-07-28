import pytest
import pandas as pd
from mls_lib.feature_engineering import ColumnConcat
from mls_lib.objects.data_frame import DataFrame
from unittest.mock import patch


# --- Pytest Fixtures ---

@pytest.fixture
def column_concat_instance():
    """Provides a fresh instance of ColumnConcat."""
    return ColumnConcat()

@pytest.fixture
def sample_left_pandas_df():
    """Provides a sample pandas DataFrame for the left table."""
    return pd.DataFrame({
        'L_col_A': [1, 2, 3],
        'L_col_B': ['X', 'Y', 'Z']
    })

@pytest.fixture
def sample_right_pandas_df():
    """Provides a sample pandas DataFrame for the right table."""
    return pd.DataFrame({
        'R_col_C': [10.0, 20.0, 30.0],
        'R_col_D': [True, False, True]
    })

@pytest.fixture
def mls_lib_dataframe(pandas_df: pd.DataFrame) -> DataFrame:
    """
    Helper fixture to create an mls_lib.objects.data_frame.DataFrame instance
    from a pandas DataFrame.
    """
    df = DataFrame()
    df.set_data(pandas_df)
    return df

# --- Pytest Test Cases ---

def test_column_concat_init(column_concat_instance):
    """Test the constructor of ColumnConcat."""
    assert isinstance(column_concat_instance.left_table, DataFrame)
    assert isinstance(column_concat_instance.right_table, DataFrame)
    # Initially, their internal pandas data should be None
    assert column_concat_instance.left_table.get_data() is None
    assert column_concat_instance.right_table.get_data() is None

def test_column_concat_set_data(column_concat_instance, sample_left_pandas_df, sample_right_pandas_df):
    """Test the set_data method of ColumnConcat."""
    left_df_obj = DataFrame()
    left_df_obj.set_data(sample_left_pandas_df)
    right_df_obj = DataFrame()
    right_df_obj.set_data(sample_right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    assert column_concat_instance.left_table is left_df_obj
    assert column_concat_instance.right_table is right_df_obj
    pd.testing.assert_frame_equal(column_concat_instance.left_table.get_data(), sample_left_pandas_df)
    pd.testing.assert_frame_equal(column_concat_instance.right_table.get_data(), sample_right_pandas_df)

def test_column_concat_execute_basic_concat(column_concat_instance, sample_left_pandas_df, sample_right_pandas_df):
    """Test the execute method with two non-empty dataframes."""
    # Prepare mls_lib DataFrame instances
    left_df_obj = DataFrame()
    left_df_obj.set_data(sample_left_pandas_df)
    right_df_obj = DataFrame()
    right_df_obj.set_data(sample_right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    # Patch the _set_output method of the ColumnConcat instance
    with patch.object(column_concat_instance, '_set_output') as mock_set_output:
        column_concat_instance.execute()

        # Verify _set_output was called exactly once
        mock_set_output.assert_called_once()

        # Get the arguments passed to _set_output
        call_args, call_kwargs = mock_set_output.call_args
        output_key = call_args[0]
        output_dataframe_wrapper = call_args[1]

        assert output_key == "selected_table"
        assert isinstance(output_dataframe_wrapper, DataFrame)

        expected_concatenated_data = pd.concat([sample_left_pandas_df, sample_right_pandas_df], axis=1)

        pd.testing.assert_frame_equal(output_dataframe_wrapper.get_data(), expected_concatenated_data)

def test_column_concat_execute_empty_left_table(column_concat_instance, sample_right_pandas_df):
    """Test execute with an empty left table."""
    empty_left_pandas_df = pd.DataFrame(columns=['L_col_A', 'L_col_B']) # Empty but with columns
    left_df_obj = DataFrame()
    left_df_obj.set_data(empty_left_pandas_df)
    right_df_obj = DataFrame()
    right_df_obj.set_data(sample_right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    with patch.object(column_concat_instance, '_set_output') as mock_set_output:
        column_concat_instance.execute()

        mock_set_output.assert_called_once()
        output_dataframe_wrapper = mock_set_output.call_args[0][1]

        expected_concatenated_data = pd.concat([empty_left_pandas_df, sample_right_pandas_df], axis=1)
        pd.testing.assert_frame_equal(output_dataframe_wrapper.get_data(), expected_concatenated_data)

def test_column_concat_execute_empty_right_table(column_concat_instance, sample_left_pandas_df):
    """Test execute with an empty right table."""
    left_df_obj = DataFrame()
    left_df_obj.set_data(sample_left_pandas_df)
    empty_right_pandas_df = pd.DataFrame(columns=['R_col_C', 'R_col_D']) # Empty but with columns
    right_df_obj = DataFrame()
    right_df_obj.set_data(empty_right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    with patch.object(column_concat_instance, '_set_output') as mock_set_output:
        column_concat_instance.execute()

        mock_set_output.assert_called_once()
        output_dataframe_wrapper = mock_set_output.call_args[0][1]

        expected_concatenated_data = pd.concat([sample_left_pandas_df, empty_right_pandas_df], axis=1)
        pd.testing.assert_frame_equal(output_dataframe_wrapper.get_data(), expected_concatenated_data)

def test_column_concat_execute_both_tables_empty(column_concat_instance):
    """Test execute with both tables being empty."""
    empty_left_pandas_df = pd.DataFrame(columns=['L_col_A'])
    left_df_obj = DataFrame()
    left_df_obj.set_data(empty_left_pandas_df)

    empty_right_pandas_df = pd.DataFrame(columns=['R_col_C'])
    right_df_obj = DataFrame()
    right_df_obj.set_data(empty_right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    with patch.object(column_concat_instance, '_set_output') as mock_set_output:
        column_concat_instance.execute()

        mock_set_output.assert_called_once()
        output_dataframe_wrapper = mock_set_output.call_args[0][1]

        expected_concatenated_data = pd.DataFrame(columns=['L_col_A', 'R_col_C'])
        pd.testing.assert_frame_equal(output_dataframe_wrapper.get_data(), expected_concatenated_data, check_dtype=False)

def test_column_concat_execute_with_index_mismatch(column_concat_instance):
    """
    Test execute when indices don't align. Pandas concat by default aligns on index.
    This test verifies pandas' default behavior is used.
    """
    left_pandas_df = pd.DataFrame({'L_data': [1, 2, 3]}, index=[0, 1, 2])
    right_pandas_df = pd.DataFrame({'R_data': [10, 20, 30]}, index=[1, 2, 3]) # Mismatched index

    left_df_obj = DataFrame()
    left_df_obj.set_data(left_pandas_df)
    right_df_obj = DataFrame()
    right_df_obj.set_data(right_pandas_df)

    column_concat_instance.set_data(left_df_obj, right_df_obj)

    with patch.object(column_concat_instance, '_set_output') as mock_set_output:
        column_concat_instance.execute()

        mock_set_output.assert_called_once()
        output_dataframe_wrapper = mock_set_output.call_args[0][1]

        # Pandas default behavior for concat axis=1 with non-matching index is outer join on index
        expected_concatenated_data = pd.concat([left_pandas_df, right_pandas_df], axis=1)
        pd.testing.assert_frame_equal(output_dataframe_wrapper.get_data(), expected_concatenated_data)