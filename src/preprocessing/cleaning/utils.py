import pandas as pd


def handle_unknowns(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[~df.CAUSE_CLASS.isin(["Human", "Natural"]), ["CAUSE_CLASS"]] = "Unknown"

    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = pd.Categorical(df[col].fillna("Unknown"))

    return df


def prune_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols_to_drop = (
        df.iloc[:, : df.columns.get_loc("COMPLEX_NAME")].columns.tolist()
        + ["FIRE_YEAR", "DISCOVERY_DOY", "CONT_DOY", "OWNER_DESCR"]
        + list(df.columns[-5:-2])
    )
    return df.drop(cols_to_drop, axis=1)
