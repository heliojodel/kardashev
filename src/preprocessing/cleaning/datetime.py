from datetime import datetime

import pandas as pd


def fix_datetime(
    df: pd.DataFrame,
    col_prefix: str | list,
    time_format: str = "%H%M",
) -> pd.DataFrame:
    prefixes = [col_prefix] if isinstance(col_prefix, str) else col_prefix
    prefix_len = prefixes.__len__()
    for prefix in prefixes[:prefix_len]:
        col_date, col_time = f"{prefix}_DATE", f"{prefix}_TIME"

        df[col_date] = pd.to_datetime(df[col_date])
        df_time = df[col_time].astype(int, errors="ignore").astype(str).str.zfill(4)
        df[col_time] = pd.to_datetime(
            df_time, format=time_format, errors="coerce"
        ).dt.time

        def combine_date_time(row):
            return (
                datetime.combine(row[col_date], row[col_time])
                if pd.notnull(row[col_time])
                else row[col_date]
            )

        df_dt = df.apply(combine_date_time, axis=1)
        col_dt = f"{prefix}_DATETIME"

        try:
            df[col_dt] = pd.to_datetime(df_dt, errors="raise")
        except pd.errors.OutOfBoundsDatetime:
            df[col_dt] = pd.to_datetime(df_dt, errors="coerce")
            mask = df[col_dt].isna()
            df.loc[mask, col_dt] = df.loc[mask, "DISCOVERY_DATE"]

        prefixes.extend([col_date, col_time])
    df.drop(columns=prefixes[prefix_len:], inplace=True)

    return df
