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
