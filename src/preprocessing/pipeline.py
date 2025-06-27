import pandas as pd
from src.cleaning.clean import clean as clean_data
from src.features.engineering import add_duration


def preprocess(input_path: str, output_path: str = None) -> pd.DataFrame:
    """
    Preprocessing pipeline that:
      1. Loads raw data.
      2. Cleans the data using the cleaning module.
      3. Applies feature engineering.

    Args:
        input_path (str): Path to the raw CSV file.
        output_path (str, optional): Path to save the processed data.

    Returns:
        pd.DataFrame: The fully preprocessed dataframe.
    """
    # Load raw data
    df = pd.read_csv(input_path)

    # Cleaning step
    df_clean = clean_data(df)

    # Convert datetime columns to proper datetime types if not already done
    df_clean["DISCOVERY_DATETIME"] = pd.to_datetime(df_clean["DISCOVERY_DATETIME"])
    df_clean["CONT_DATETIME"] = pd.to_datetime(df_clean["CONT_DATETIME"])

    # Feature engineering step
    df_features = add_duration(df_clean)

    return df_features


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the preprocessing pipeline.")
    parser.add_argument("--input", required=True, help="Path to the input CSV file")
    args = parser.parse_args()

    processed_df = preprocess(args.input, args.output)
    print("Preprocessing complete. Processed data shape:", processed_df.shape)
