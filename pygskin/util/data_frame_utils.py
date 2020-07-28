
def dict_from_data_frame_columns(df, key_col, value_col):
    if key_col is None or key_col not in df.columns:
        raise ValueError(f"The column, {key_col}, is not found in data frame")
    if value_col is None or value_col not in df.columns:
        raise ValueError(f"The column, {value_col}, is not found in data frame")
    return list(df[[key_col, value_col]].set_index(key_col).to_dict().values())[0]


def col_contains_all_values(df, col, values):
    if col is None or col not in df.columns:
        raise ValueError(f"The column, {col}, must be found in data frame")
    return all(val in values for val in df[col].unique())
