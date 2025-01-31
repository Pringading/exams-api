import pandas as pd
import pytest
from db.utils.edexcel_data import (
    excel_to_df,
    split_examination_code_col,
    convert_time_to_am_pm,
    update_edexcel_column_names,
    edexcel_data_to_df
)


class TestExcelToDF:
    """Testing excel_to_df function in db/utils/edexcel_data.py file"""

    @pytest.mark.it('Test excel to df function returns a dataframe')
    def test_excel_to_df_returns_df(self):
        """Testing that the return value is a pandas dataframe"""

        result = excel_to_df("db/data/Edexcel_GCE.xlsx")
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it('Test excel to df returns dataframe with the expected ' +
                    'columns')
    def test_excel_to_df_columns(self):
        """Testing that the returned dataframe has the expected columns"""

        expected_columns = [
            'Date', 'Exam series', 'Board', 'Examination code',
            'Subject', 'Title', 'Time', 'Duration'
        ]
        result = excel_to_df("test/data/test_edexcel_gcse.xlsx")
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

        Uses test_df fixture."""

        result = split_examination_code_col(test_df)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it('Test returned df has Syllabus Code and Component Code ' +
                    'functions')
    def test_returned_columns(self, test_df):
        """Testing adds two columns with the expected names to the dataframe

        uses test_df fixture."""

        result = split_examination_code_col(test_df)
        assert 'syllabus_code' in result.columns
        assert 'component_code' in result.columns

    @pytest.mark.it('Test syllabus code column has expected values')
    def test_syllabus_code_values(self, test_df):
        """Testing syllabus_code column extracts values before the space in
        Examination code column of given dataframe.

        uses test_df fixture"""

        expected = ["exam1", "exam2", "exam3"]
        result = split_examination_code_col(test_df)
        assert result["syllabus_code"].tolist() == expected

    @pytest.mark.it('Test component code column has expected values')
    def test_component_code_values(self, test_df):
        """Testing syllabus_code column extracts values after the space in
        in Examination code column of given dataframe.

        uses test_df fixture"""

        expected = ["01", "02", "03"]
        result = split_examination_code_col(test_df)
        assert result["component_code"].tolist() == expected


class TestConvertTimeToAMPM:
    """Testing convert_time_to_am_pm function inside data/edexcel_data.py"""

    @pytest.mark.it('Returns dataframe')
    def test_returns_df(self):
        """Testing return value is a pandas dataframe object."""

        test_df = pd.DataFrame({'Time': []})
        result = convert_time_to_am_pm(test_df)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it('Time column has AM and PM instead of Morning and' +
                    ' Afternoon')
    def test_time_column_has_expected_values(self):
        """Testing returned dataframe converts 'Morning' to 'AM' and
        'Afternoon' to 'PM' in Time column of given dataframe."""

        test_df = pd.DataFrame({'Time': ['Morning', 'Afternoon', 'Morning']})
        expected = ['AM', 'PM', 'AM']
        result = convert_time_to_am_pm(test_df)
        assert result['Time'].tolist() == expected

    @pytest.mark.it('Time column has ignores values that aren\'t Morning or' +
                    ' Afternoon')
    def test_other_values(self):
        """Testing returned dataframe shows any values other than Morning
        or Afternoon as null."""

        test_df = pd.DataFrame({
            'Time': ['Morning', 'Afternoon', 'Other', 'Morning']
        })
        expected = ['AM', 'PM', None, 'AM']
        result = convert_time_to_am_pm(test_df)
        assert result['Time'].tolist() == expected


class TestUpdateExcelColumnNames:
    @pytest.fixture
    def test_df(self):
        """Test dataframe with necessary columns from Excel sheet. Omits
        any columns not accessed by update_excel_column_names function."""

        df = pd.DataFrame()
        df['syllabus_code'] = ["syllabus1"]
        df['component_code'] = ["component1"]
        df['Date'] = ["2060-01-01"]
        df['Board'] = ["Pearson"]
        df['Subject'] = ["Subject1"]
        df['Title'] = ["Title1"]
        df['Time'] = ["AM"]
        df['Duration'] = ["1h 30m"]
        return df

    @pytest.mark.it('Test returns dataframe.')
    def test_returns_df(self, test_df):
        """Testing function returns a pandas DataFrame object.

        uses test_df fixture."""

        result = update_edexcel_column_names(test_df)
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.it('Test returns dataframe with expected columns')
    def test_returns_expected_columns(self, test_df):
        """Testing returned dataframe has columns needed for the exams table
        in the destination database.

        uses test_df fixture."""

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
        """Checking expected data is in expected column.

        uses test_df."""

        result = update_edexcel_column_names(test_df)
        assert result['syllabus_code'].tolist() == ["syllabus1"]
        assert result['component_code'].tolist() == ["component1"]
        assert result['date'].tolist() == ["2060-01-01"]
        assert result['board'].tolist() == ["Pearson"]
        assert result['subject'].tolist() == ["Subject1"]
        assert result['title'].tolist() == ["Title1"]
        assert result['time'].tolist() == ["AM"]
        assert result['duration'].tolist() == ["1h 30m"]


class TestExcelDataToDF:
    @pytest.mark.it('Test excel data to df transforms data from excel ' +
                    'spreadsheet to expected format.')
    def test_calls_excel_to_df(self):
        result = edexcel_data_to_df("test/data/test_edexcel_gcse.xlsx")
        assert result['syllabus_code'].tolist() == ["TEST"] * 3
        assert result['component_code'].tolist() == ["01", "02", "03"]
        assert result['date'].astype(str).tolist() == ["2025-05-22"] * 3
        assert result['board'].tolist() == ["Pearson"] * 3
        assert result['subject'].tolist() == ["GCSE Test"] * 3
        assert result['title'].tolist() == [
            "Test Exam 1", "Test Exam 2", "Test Exam 3"
        ]
        assert result['time'].tolist() == ["PM", "AM", "PM"]
        assert result['duration'].tolist() == ["0h 35m", "1h 45m", "2h"]
