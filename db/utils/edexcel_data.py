import pandas as pd

EXCEL_GCE_DATA = "db/data/Edexcel_GCE.xlsx"
EXCEL_GCSE_DATA = "db/data/Edexcel_GCSE.xlsx"


def excel_to_df(filepath: str, sheet:int=2) -> pd.DataFrame:
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

# split examination code into 2 columns
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