import pandas as pd

EDEXCEL_GCE_DATA = "db/data/Edexcel_GCE.xlsx"
EDEXCEL_GCSE_DATA = "db/data/Edexcel_GCSE.xlsx"


def excel_to_df(filepath: str, sheet: int = 2) -> pd.DataFrame:
    """Takes excel sheet and converts to a dataframe.

    Args:
        filepath (str): path to the excel file.
        sheet (int): within the excel workbook, the number of the sheet to
            obtain the data from. Sheets are 0-indexed & the same order as the
            tabs along the bottom.

    Returns:
        Data from the sheet as a pandas dataframe.
    """

    df = pd.read_excel(filepath, sheet_name=sheet)
    return df


def split_examination_code_col(df: pd.DataFrame) -> pd.DataFrame:
    """Splits Examination code into 2 columns, using space as a delimiter

    Args:
        df (DataFrame): With 'Examination code' column made up
            column is 2 strings with a space eg. "9MA0 01"

    Returns:
        same DataFrame with 2 new columns: Syllabus code and Component Code
            eg. syllabus_code = "9MAO
                component_code = "01"
    """

    df['syllabus_code'] = df['Examination code'].str.split().str[0]
    df['component_code'] = df["Examination code"].str.split().str[1]
    return df


def convert_time_to_am_pm(df: pd.DataFrame) -> pd.DataFrame:
    """Converts Time column from Morning/Afternoon to AM/PM

    Args:
        df(DataFrame) with 'Time' column with values 'Morning' and 'Afternoon'

    Returns: DataFrame with 'Time' column with values 'AM', 'PM' or null
    """

    lookup = {'Morning': 'AM', 'Afternoon': 'PM'}
    times = df['Time'].tolist()
    df['Time'] = [lookup[time] if time in lookup else None for time in times]
    return df


def update_edexcel_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Returns dataframe with same column names as the destination database.

    Args:
        df (DataFrame): which includes following columns:
            syllabus_code, component_code, Date,
            Board, Subject, Title, Time, Duration

    Returns:
        Dataframe with following columns:
            syllabus_code, component_code, board, subject, title, date, time,
            duration
    """

    new_df = pd.DataFrame()
    new_df['syllabus_code'] = df['syllabus_code']
    new_df['component_code'] = df['component_code']
    new_df['board'] = df['Board']
    new_df['subject'] = df['Subject']
    new_df['title'] = df['Title']
    new_df['date'] = df['Date']
    new_df['time'] = df['Time']
    new_df['duration'] = df['Duration']
    return new_df
