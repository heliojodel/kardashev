import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import sqlite3
import json, yaml
from typing import Any
import pandas as pd
from pathlib import Path


def encoder_data(encoder, **kwargs):
    return encoder(**kwargs)


def fit_data(encoder, features, labels=None, **kwargs):
    return encoder.fit(features, labels, **kwargs)


def transf_data(encoder, features, **kwargs):
    return encoder.transform(features, **kwargs)


def encode_data(encoder, features, labels=None, fit_args=None, transf_args=None):
    encoder.fit(features, labels, **(transf_args | {}))
    return encoder.transform(features, **(transf_args | {}))


def load_data(input_path: Path, **args) -> ...:
    ext = input_path.suffix.lstrip(".")

    match ext:
        case "parquet":
            return pd.read_parquet(input_path, **args)
        case "json":
            with open(input_path, "r", encoding=args.get("encoding", "utf-8")) as f:
                return json.load(f, **args)
        case "yaml" | "yml":
            with open(input_path, "r", encoding=args.get("encoding", "utf-8")) as f:
                return yaml.safe_load(f, **args)
        case "sqlite":
            conn = sqlite3.connect(input_path)
            try:
                return pd.read_sql("SELECT * FROM Fires", conn, **args)
            finally:
                conn.close()
        case _:
            return pd.read_csv(input_path, **args)


def save_data(data: ..., output_path: Path, *, index: bool = False, **args) -> Any:
    ext = output_path.suffix.lstrip(".")
    match ext:
        case "parquet":
            return data.to_parquet(output_path, index=index, **args)
        case "json":
            with open(output_path, "w", encoding=args.get("encoding", "utf-8")) as fp:
                return json.dump(data, f, **args)
        case "yaml" | "yml":
            with open(output_path, "w", encoding=args.get("encoding", "utf-8")) as fp:
                return yaml.dump(data, f, **args)
        case _:
            return data.to_csv(output_path, index=index, **args)


def split_data(
    df: pd.DataFrame,
    y: str = "CAUSE_CLASS",
    class_type: str = "binary",
    test_size: float = 0.2,
    random_state: int = 37,
) -> list:
    """Encode label and split data

    Args:
        df (pd.DataFrame): _description_
        y (str, optional): _description_. Defaults to 'CAUSE_CLASS'.
        class_type (str, optional): _description_. Defaults to 'binary'.
        test_size (float, optional): _description_. Defaults to 0.2.
        random_state (int, optional): _description_. Defaults to 37.

    Returns:
        list: X_train, X_test, y_train, y_test
    """
    mapping = {"Human": 1, "Natural": 0}
    features = df[["FIRE_SIZE", "LATITUDE", "LONGITUDE"]]
    target = (
        LabelEncoder().fit_transform(df[y])
        if class_type == "multiclass"
        else df[y].map(mapping).copy()
    )
    return train_test_split(
        features, target, test_size=test_size, random_state=random_state
    )


def undersample(df: pd.DataFrame, n_samples: int = None) -> pd.DataFrame:
    """Return a data with same amount of both classes

    Args:
        df (pd.DataFrame): _description_
        n_samples (int, optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    df_class0 = df[df.CAUSE_CLASS == "Human"]
    df_class1 = df[df.CAUSE_CLASS == "Natural"]

    if n_samples is None:
        n_samples = min(df.CAUSE_CLASS.value_counts().values)

    df_class0_down = df_class0.sample(n=n_samples, random_state=37)
    df_class1_down = df_class1.sample(n=n_samples, random_state=37)

    balanced_df = (
        pd.concat([df_class0_down, df_class1_down])
        .sample(frac=1, random_state=37)
        .reset_index(drop=True)
    )
    return balanced_df
