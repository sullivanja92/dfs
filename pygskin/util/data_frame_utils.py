
def dict_from_data_frame_columns(df, key_col, value_col):
    if key_col is None or key_col not in df.columns:
        raise ValueError(f"The column, {key_col}, is not found in data frame")
    if value_col is None or value_col not in df.columns:
        raise ValueError(f"The column, {value_col}, is not found in data frame")
    return list(df[[key_col, value_col]].set_index(key_col).to_dict().values())[0]


def contains_all_columns(df, columns):
    if df is None or columns is None:
        raise ValueError("Data frame and columns must not be None")
    return all([x in df.columns for x in columns])


def col_contains_all_values(df, col, values):
    if col is None or col not in df.columns:
        raise ValueError(f"The column, {col}, must be found in data frame")
    return all(val in df[col].unique() for val in values)
