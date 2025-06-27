import pandas as pd
import numpy as np


def add_duration(df, start_col="DISCOVERY_DATETIME", end_col="CONT_DATETIME"):
    df["DURATION"] = (df[end_col] - df[start_col]).dt.total_seconds() / 3600
    return df


def add_weekend_flag(df, datetime_col="DISCOVERY_DATETIME"):
    df["IS_WEEKEND"] = df[datetime_col].dt.dayofweek >= 5
    df["IS_WEEKEND"] = df.IS_WEEKEND.convert_dtypes()
    return df


def add_time_of_day(df, datetime_col="DISCOVERY_DATETIME"):
    def time_of_day(hour):
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    df["TIME_OF_DAY"] = df[datetime_col].dt.hour.apply(time_of_day).astype("category")
    return df


def add_season(df, datetime_col="DISCOVERY_DATETIME"):
    def season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df["SEASON"] = df[datetime_col].dt.month.apply(season).astype("category")
    return df


def add_time_since_prev(df, datetime_col="DISCOVERY_DATETIME"):
    df = df.sort_values(datetime_col)
    df["HOURS_SINCE_PREV"] = df[datetime_col].diff().dt.total_seconds() / 3600
    df["HOURS_SINCE_PREV"].fillna(0, inplace=True)
    df["HOURS_SINCE_PREV"] = pd.to_numeric(df["HOURS_SINCE_PREV"])
    df.sort_index(inplace=True)
    return df


def add_spread_rate(df, fire_size_col="FIRE_SIZE", duration_col="DURATION"):
    df["SPREAD_RATE"] = df.apply(
        lambda row: row[fire_size_col] / row[duration_col]
        if row[duration_col] > 0
        else 0,
        axis=1,
    )
    return df
