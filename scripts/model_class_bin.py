#!/usr/bin/env python3
"""
Entry point for training the model.
This script uses the modularized pipeline from the src/modeling package.
"""

from src.modeling.training import model
from src.modeling.utils import setup_logging
from src.preprocessing.utils import load_data, undersample
import joblib


def main():
    # Set up logging to track progress and any issues
    # setup_logging(log_file="logs/modeling.log")

    # Define paths (consider moving these to a config file for flexibility)
    data_path = "data/interim/wildfire_human_reassigned.csv"
    # model_save_path = "models/best_model_bin.pkl"

    # Train the model and save the best estimator

    df = load_data(data_path)
    mask = df["CAUSE_CLASS"].isin(["Human", "Natural"])
    data = undersample(df[mask])
    pipeline = model(data, mask, params_path="models/best_sgd_params.pkl")
    joblib.dump(pipeline, "models/best_sgd_model.pkl")

    print("Training complete. Model SGD saved")


if __name__ == "__main__":
    main()
