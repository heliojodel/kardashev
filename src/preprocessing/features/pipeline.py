import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from src.preprocessing.features.engineering import (
    add_duration,
    add_season,
    add_spread_rate,
    add_time_of_day,
    add_time_since_prev,
    add_weekend_flag,
)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        start_col="DISCOVERY_DATETIME",
        end_col="CONT_DATETIME",
        datetime_col="DISCOVERY_DATETIME",
        fire_size_col="FIRE_SIZE",
    ):
        self.start_col = start_col
        self.end_col = end_col
        self.datetime_col = datetime_col
        self.fire_size_col = fire_size_col

    def fit(self, X, y=None):
        return self

    def transform(self, df):
        df = add_duration(df, start_col=self.start_col, end_col=self.end_col)
        df = add_weekend_flag(df, datetime_col=self.datetime_col)
        df = add_time_of_day(df, datetime_col=self.datetime_col)
        df = add_season(df, datetime_col=self.datetime_col)
        df = add_time_since_prev(df, datetime_col=self.datetime_col)
        df = add_spread_rate(
            df, fire_size_col=self.fire_size_col, duration_col="DURATION"
        )

        return df