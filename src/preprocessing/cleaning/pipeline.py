import pandas as pd

from .categorical import fix_categorical
from .datetime import fix_datetime
from .numeric import fix_numeric
from .utils import handle_unknowns, prune_columns


class Cleaner:
    def __init__(self):
        pass

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._rename_columns(df)
        df = self._fix_datetime(df)
        df = self._fix_categorical(df)
        df = self._fix_numeric(df)
        df = self._fix_causes(df)
        df = self._handle_unknowns(df)
        df = self._prune_columns(df)
        df = df.drop_duplicates()

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(
            columns={
                "NWCG_CAUSE_CLASSIFICATION": "CAUSE_CLASS",
                "NWCG_GENERAL_CAUSE": "CAUSE",
                "NWCG_CAUSE_AGE_CATEGORY": "CAUSE_AGE",
            }
        )

    def _fix_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        return fix_datetime(df, ["DISCOVERY", "CONT"])

    def _fix_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        return fix_categorical(df, "COMPLEX_NAME")

    def _fix_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        return fix_numeric(df, ["FIRE_SIZE"])

    def _fix_causes(self, df: pd.DataFrame) -> pd.DataFrame:
        mode_cause = df.CAUSE.mode()[0]
        df.loc[(df.CAUSE_CLASS == "Human") & (df.CAUSE == mode_cause), "CAUSE"] = (
            "Human but unspecified causes"
        )

        df["CAUSE"] = df["CAUSE"].replace(
            {
                "Arson/incendiarism": "Arson",
                "Power generation/transmission/distribution": "Power generation and distribution",
                "Missing data/not specified/undetermined": "Unknown",
            }
        )

        return df

    def _handle_unknowns(self, df: pd.DataFrame) -> pd.DataFrame:
        return handle_unknowns(df)

    def _prune_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return prune_columns(df)
