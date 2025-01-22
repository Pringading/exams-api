from db.utils.edexcel_data import excel_to_df
from pandas import DataFrame
import pytest

@pytest.mark.it('Test excel to df function returns a dataframe')
def test_excel_to_df_returns_df():
    result = excel_to_df("db/data/Edexcel_GCE.xlsx")
    assert isinstance(result, DataFrame)



