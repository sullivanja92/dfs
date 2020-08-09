
def contains_all_columns(df, columns):
    if df is None or columns is None:
        raise ValueError("Data frame and columns must not be None")
    return all([x in df.columns for x in columns])


def col_contains_all_values(df, col, values):
    if col is None or col not in df.columns:
        raise ValueError(f"The column, {col}, must be found in data frame")
    return all(val in df[col].unique() for val in values)


def map_index_to_col(df, col):
    if df is None:
        raise ValueError('Data frame cannot be None')
    if col is None or col not in df.columns:
        raise ValueError('The column must not be None and must be found in the data frame')
    return {i: df.loc[i][col] for i in df.index}
