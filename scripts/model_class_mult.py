#!/usr/bin/env python3
"""
Entry point for training the multiclass model and generating an assigned CSV.
This script trains the model, then uses it to reassign labels on the dataset,
creating a new CSV file with the predictions.
"""

from src.modeling.training import model
from src.preprocessing.utils import load_data
from src.utils import assign
import joblib
import pandas as pd

# def reassign_multiclass(df, estimator, features=["FIRE_SIZE", "LATITUDE", "LONGITUDE"]):
#     """
#     Uses the trained estimator to generate predictions for multiclass labels
#     and adds a new column 'CAUSE_CLASS_ASSIGNED' to the dataframe.
#     """
#     # Get the predicted multiclass labels using the provided features.
#     df["CAUSE_CLASS"] = estimator.predict(df[features])
#     return df


def main():
    # Define file paths.
    data_path = "data/interim/wildfire_natural_reassigned.csv"
    # model_save_path = "models/best_model_mult.pkl"

    # Train the multiclass model.
    # Note: the train_model function is designed to load data from data_path.
    # model = train_model(data_path, model_save_path, class_type="multiclass", downsample=True)
    # print("Multiclass model training complete. Model saved at:", model_save_path)

    # Load the full dataset for assignment.
    df = load_data(data_path)

    # Reassign predictions using the trained model.

    # df["DISCOVERY_DATETIME"] = pd.to_datetime(df["DISCOVERY_DATETIME"])
    # df["CONT_DATETIME"] = pd.to_datetime(df["CONT_DATETIME"])
    pipeline = model(
        df,
        (df.CAUSE_CLASS == "Human") & (df.CAUSE != "Human but unspecified causes"),
        y="CAUSE",
        class_type="multiclass",
        n_sample=100000,
    )
    joblib.dump(pipeline, "models/best_pycaret_model.pkl")

    # Save the resulting DataFrame to a new CSV file.
    # assigned_csv_path = "data/interim/wildfire_clean_mult_assigned.csv"
    # df_assigned.to_csv(assigned_csv_path, index=False)
    # print("Assigned CSV saved at:", assigned_csv_path)


if __name__ == "__main__":
    main()
