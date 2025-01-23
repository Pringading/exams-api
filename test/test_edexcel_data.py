import pandas as pd
import pytest
from db.utils.edexcel_data import (
    excel_to_df, 
    split_examination_code_col, 
    update_edexcel_column_names
)


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


class TestUpdateExcelColumnNames:
    @pytest.fixture
    def test_df(self):
        df = pd.DataFrame()
        df['syllabus_code'] = ["code1"]
        df['component_code'] = ["code1"]
        df['Date'] = ["2060-01-01"]
        df['Board'] = ["Pearson"]
        df['Subject'] = ["Subject1"]
        df['Title'] = ["Title1"]
        df['Time'] = ["AM"]
        df['Duration'] = ["1h 30m"]
        return df


    @pytest.mark.it('Test returns dataframe.')
    def test_returns_df(self, test_df):

        result = update_edexcel_column_names(test_df)
        assert isinstance(result, pd.DataFrame)
    
    @pytest.mark.it('Test returns dataframe with expected columns')
    def test_returns_expected_columns(self, test_df):
        expected_columns = [
            'syllabus_code',
            'component_code',
            'board',
            'subject',
            'title',
            'date',
            'time',
            'duration'
        ]
        result = update_edexcel_column_names(test_df)
        for column in expected_columns:
            assert column in result.columns
        assert len(result.columns) == len(expected_columns)
    

    @pytest.mark.it('Test returns expected data')
    def test_returns_expected_data(self, test_df):
        result = update_edexcel_column_names(test_df)
        assert result['syllabus_code'].tolist() == ["code1"]
        assert result['component_code'].tolist() == ["code1"]
        assert result['date'].tolist() == ["2060-01-01"]
        assert result['board'].tolist() == ["Pearson"]
        assert result['subject'].tolist() == ["Subject1"]
        assert result['title'].tolist() == ["Title1"]
        assert result['time'].tolist() == ["AM"]
        assert result['duration'].tolist() == ["1h 30m"]

