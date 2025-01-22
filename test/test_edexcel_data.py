from db.utils.edexcel_data import excel_to_df, split_examination_code_col
import pandas as pd
import pytest


class TestExcelToDF:
    """Testing excel_to_df function from the db/utils/edexcel_data.py workbook"""

    @pytest.mark.it('Test excel to df function returns a dataframe')
    def test_excel_to_df_returns_df(self):
        """Testing that the return value is a pandas dataframe"""

        result = excel_to_df("db/data/Edexcel_GCE.xlsx")
        assert isinstance(result, pd.DataFrame)


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
        
        
class TestSplitExaminationCode:
    "Test split_examination_code_col function from db/utils/edexcel_data.py"

    @pytest.fixture
    def test_df(self):
        """Returns data frame with one column,'Examination Code' and 3 rows"""

        df = pd.DataFrame({
            "Examination code": ["exam1 01", "exam2 02", "exam3 03"]
        })
        return df

    @pytest.mark.it('Test split_examination_code_col returns dataframe')
    def test_split_exam_code_returns_df(self, test_df):
        """Test that split_examination_code_col function returns a datafame
        uses test_df fixture."""

        result = split_examination_code_col(test_df)
        assert isinstance(result, pd.DataFrame)

    
    @pytest.mark.it('Test returned df has Syllabus Code and Component Code ' +
        'functions')
    def test_returned_columns(self, test_df):
        
        result = split_examination_code_col(test_df)
        assert 'syllabus_code' in result.columns
        assert 'component_code' in result.columns
    

    @pytest.mark.it('Test syllabus code column has expected values')
    def test_syllabus_code_values(self, test_df):
        expected = ["exam1", "exam2", "exam3"]
        result = split_examination_code_col(test_df)
        assert result["syllabus_code"].tolist() == expected

    
    @pytest.mark.it('Test component code column has expected values')
    def test_component_code_values(self, test_df):
        expected = ["01", "02", "03"]
        result = split_examination_code_col(test_df)
        assert result["component_code"].tolist() == expected
