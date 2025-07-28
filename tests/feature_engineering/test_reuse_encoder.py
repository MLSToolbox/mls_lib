import pytest
import pandas as pd
from unittest.mock import patch
from mls_lib.feature_engineering import ReuseEncoder
from mls_lib.objects.data_frame import DataFrame
from mls_lib.objects.encoders.iencoder import IEncoder
# --- Pytest Fixtures ---

@pytest.fixture
def sample_pandas_dataframe():
    """Provides a sample pandas DataFrame for testing encoding."""
    return pd.DataFrame({
        'feature_num': [1, 2, 3],
        'feature_cat': ['A', 'B', 'A'],
        'another_col': [10, 20, 30]
    })

@pytest.fixture
def mock_dataframe_instance(sample_pandas_dataframe):
    """Provides a MockDataFrame instance pre-loaded with data."""
    mock_df = DataFrame()
    mock_df.set_data(sample_pandas_dataframe.copy())
    return mock_df

@pytest.fixture
def reuse_encoder_instance():
    """Provides an instance of ReuseEncoder."""
    return ReuseEncoder()


# --- Pytest Test Cases ---

def test_reuse_encoder_init(reuse_encoder_instance):
    """Test the constructor of ReuseEncoder."""
    assert isinstance(reuse_encoder_instance.data, DataFrame)
    assert isinstance(reuse_encoder_instance.encoder, IEncoder)
    assert reuse_encoder_instance.data.get_data() is None

def test_reuse_encoder_set_data(reuse_encoder_instance, mock_dataframe_instance):
    """Test the set_data method of ReuseEncoder."""
    reuse_encoder_instance.set_data(mock_dataframe_instance, IEncoder())
    assert reuse_encoder_instance.data is mock_dataframe_instance