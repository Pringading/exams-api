from pg8000 import Connection


def data_to_dict_list(data: list[list], columns: list[dict]) -> list[dict]:
    """Takes data and columns from a SQL query and returns list of dicts.
    
    Args:
        data(list): rows of data as a list of lists.
        columns(list): columns of a table as a list of dictionaries, the
            name of each column is on the name key.
    
    Returns:
        list with a dictionary for each row of data, the column names are
        the keys and the original data are the values."""
    
    cols = [col['name'] for col in columns]
    result = []
    for row in data:
        result.append(dict(zip(cols, row)))
    return result
