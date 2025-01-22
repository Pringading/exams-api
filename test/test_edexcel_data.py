from db.utils.edexcel_data import excel_to_df
from pandas import DataFrame
import pytest


class TestExcelToDF:
    """Testing excel to df function from the db/utils/edexcel_data.py workbook"""

    @pytest.mark.it('Test excel to df function returns a dataframe')
    def test_excel_to_df_returns_df(self):
        """Testing that the return value is a pandas dataframe"""

        result = excel_to_df("db/data/Edexcel_GCE.xlsx")
        assert isinstance(result, DataFrame)


    @pytest.mark.it('Test excel to df returns dataframe with the expected columns')
    def test_excel_to_df_columns(self):
        """Testing that the returned dataframe has the expected columns"""

        expected_columns = [
            'Date', 'Exam series', 'Board', 'Examination code',
            'Subject', 'Title', 'Time', 'Duration'
        ]
        result = excel_to_df("db/data/Edexcel_GCE.xlsx")
        for column in expected_columns:
            assert column in result.columns
        
        
