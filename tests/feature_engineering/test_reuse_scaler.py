import pytest
import pandas as pd
from unittest.mock import patch
from mls_lib.feature_engineering import SplitDataframe
from mls_lib.objects.data_frame import DataFrame
# Assume the provided code is in a file named 'split_dataframe.py'
# from split_dataframe import SplitDataframe

# --- Pytest Suite ---

@pytest.fixture
def sample_dataframe():
    """Provides a sample pandas DataFrame for testing."""
    return pd.DataFrame({
        'col_a': [1, 2, 3],
        'col_b': [4, 5, 6],
        'col_c': [7, 8, 9]
    })

@pytest.fixture
def mock_mls_dataframe(sample_dataframe):
    """Provides a mock mls_lib.objects.data_frame.DataFrame instance."""
    mock_df = DataFrame()
    mock_df.set_data(sample_dataframe)
    return mock_df

def test_split_dataframe_init():
    """Test the constructor of SplitDataframe."""
    columns = ['col_a', 'col_c']
    splitter = SplitDataframe(columns)
    assert splitter.columns == columns
    assert isinstance(splitter.table, DataFrame)

def test_split_dataframe_set_data(mock_mls_dataframe):
    """Test the set_data method of SplitDataframe."""
    columns = ['col_a']
    splitter = SplitDataframe(columns)
    splitter.set_data(mock_mls_dataframe)
    assert splitter.table is mock_mls_dataframe
    assert splitter.table.get_data().equals(mock_mls_dataframe.get_data())

def test_split_dataframe_execute_basic_split(sample_dataframe, mock_mls_dataframe):
    """Test the execute method with a basic split."""
    columns_to_select = ['col_a', 'col_c']
    splitter = SplitDataframe(columns_to_select)
    splitter.set_data(mock_mls_dataframe)

    # We need to mock _set_output, as it's a method of the base class MockTask
    with patch.object(splitter, '_set_output') as mock_set_output:
        splitter.execute()

        # Assert that _set_output was called twice
        assert mock_set_output.call_count == 2

        # Get the arguments passed to the first call for selected_table
        call_args_selected = mock_set_output.call_args_list[0]
        assert call_args_selected.args[0] == "selected_table"
        selected_output_df = call_args_selected.args[1]
        assert isinstance(selected_output_df, DataFrame)
        expected_selected_data = sample_dataframe[columns_to_select]
        pd.testing.assert_frame_equal(selected_output_df.get_data(), expected_selected_data)

        # Get the arguments passed to the second call for unselected_table
        call_args_unselected = mock_set_output.call_args_list[1]
        assert call_args_unselected.args[0] == "unselected_table"
        unselected_output_df = call_args_unselected.args[1]
        assert isinstance(unselected_output_df, DataFrame)
        expected_unselected_data = sample_dataframe.drop(columns_to_select, axis=1)
        pd.testing.assert_frame_equal(unselected_output_df.get_data(), expected_unselected_data)

def test_split_dataframe_execute_no_selected_columns(sample_dataframe, mock_mls_dataframe):
    """Test execute when no columns are selected (empty selected_table)."""
    columns_to_select = []
    splitter = SplitDataframe(columns_to_select)
    splitter.set_data(mock_mls_dataframe)

    with patch.object(splitter, '_set_output') as mock_set_output:
        splitter.execute()

        assert mock_set_output.call_count == 2

        # Selected table should be empty
        call_args_selected = mock_set_output.call_args_list[0]
        assert call_args_selected.args[0] == "selected_table"
        selected_output_df = call_args_selected.args[1]
        assert isinstance(selected_output_df, DataFrame)

        # Unselected table should be the original data
        call_args_unselected = mock_set_output.call_args_list[1]
        assert call_args_unselected.args[0] == "unselected_table"
        unselected_output_df = call_args_unselected.args[1]
        assert isinstance(unselected_output_df, DataFrame)
        pd.testing.assert_frame_equal(unselected_output_df.get_data(), sample_dataframe)

def test_split_dataframe_execute_all_columns_selected(sample_dataframe, mock_mls_dataframe):
    """Test execute when all columns are selected (empty unselected_table)."""
    columns_to_select = ['col_a', 'col_b', 'col_c']
    splitter = SplitDataframe(columns_to_select)
    splitter.set_data(mock_mls_dataframe)

    with patch.object(splitter, '_set_output') as mock_set_output:
        splitter.execute()

        assert mock_set_output.call_count == 2

        # Selected table should be the original data
        call_args_selected = mock_set_output.call_args_list[0]
        assert call_args_selected.args[0] == "selected_table"
        selected_output_df = call_args_selected.args[1]
        assert isinstance(selected_output_df, DataFrame)
        pd.testing.assert_frame_equal(selected_output_df.get_data(), sample_dataframe)

        # Unselected table should be empty
        call_args_unselected = mock_set_output.call_args_list[1]
        assert call_args_unselected.args[0] == "unselected_table"
        unselected_output_df = call_args_unselected.args[1]
        assert isinstance(unselected_output_df, DataFrame)

def test_split_dataframe_execute_non_existent_column(mock_mls_dataframe):
    """Test execute when a non-existent column is in the selection list.
    Pandas handles this by raising a KeyError, which should propagate.
    """
    columns_to_select = ['col_a', 'non_existent_col']
    splitter = SplitDataframe(columns_to_select)
    splitter.set_data(mock_mls_dataframe)

    with pytest.raises(KeyError):
        splitter.execute()