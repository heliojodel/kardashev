import pandas as pd


def fix_categorical(
    df: pd.DataFrame, cols: str | list, case: bool = True
) -> pd.DataFrame:
    cols = [cols] if isinstance(cols, str) else cols
    for col in cols:
        df[col] = df[col].str.strip()
        if case:
            df[col] = df[col].str.upper()

    return df
