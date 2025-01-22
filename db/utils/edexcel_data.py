import pandas as pd


EXCEL_GCE_DATA = "db/data/Edexcel_GCE.xlsx"
EXCEL_GCSE_DATA = "db/data/Edexcel_GCSE.xlsx"


def excel_to_df(filepath: str, sheet:int=2) -> pd.DataFrame:
    df = pd.read_excel(filepath, sheet_name=sheet)
    return df
