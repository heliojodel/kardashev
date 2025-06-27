import pandas as pd


def fix_numeric(
    df: pd.DataFrame, cols: str | list
) -> pd.DataFrame:
    cols = [cols] if isinstance(cols, str) else cols
    for col in cols:
        df_col, cap_err= df[col], 1e-10
        df[col].clip(lower=df_col.min() + cap_err, upper=df_col.max() - cap_err, inplace=True)
 
    return df
