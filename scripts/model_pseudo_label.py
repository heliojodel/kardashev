# from src.modeling.training import train_model
from src.modeling.training import model
from src.preprocessing.utils import load_data, split_data
from src.modeling.utils import assign_trained
from src.utils import assign
from sklearn.metrics import classification_report, roc_auc_score
import pandas as pd
import numpy as np
import joblib


def iterative_labeling(
    data_path: str,
    model_save_path: str,
    params_path: str,
    threshold: float = 0.95,
    max_iter: int = 50,
    patience: int = 2,  # number of consecutive iterations with minimal change
    relative_threshold: float = 0.9,  # 10% relative change
):
    df = load_data(data_path)
    features = ["FIRE_SIZE", "LATITUDE", "LONGITUDE"]

    prev_assigned = None
    plateau_count = 0

    for iteration in range(max_iter):
        print(f"\n--- Iteration {iteration + 1}/{max_iter} ---")

        known_mask = df["CAUSE_CLASS"].isin(["Human", "Natural"])
        unknown_mask = ~known_mask

        if unknown_mask.sum() == 0:
            print("All data labeled. Exiting iterative step.")
            break

        df, num_reassigned = assign_trained(
            df, known_mask, value="Human", params_path=params_path, num_assigned=True
        )
        # X_train, X_test, y_train, y_test = split_data(df[known_mask])
        # pipeline = model(params_path=params_path)
        # pipeline.fit(X_train, y_train)
        # df, num_reassigned = assign(
        #     df, df[unknown_mask], pipeline, "Human", threshold=threshold, as_list=True
        # )

        print(f"Label reassigned in iteration {iteration + 1}: {num_reassigned}")

        # Adaptive plateau check:
        if prev_assigned is not None:
            rel_change = abs(num_reassigned - prev_assigned) / (prev_assigned + 1e-5)
            # print(rel_change*100)
            if rel_change > relative_threshold:
                plateau_count += 1
                print(
                    f"Relative change {rel_change:.4f} is above threshold; plateau count: {plateau_count}"
                )
            else:
                plateau_count = 0
        prev_assigned = num_reassigned if iteration == 1 else prev_assigned

        if plateau_count >= patience:
            print(
                f"Plateau reached for {plateau_count} consecutive iterations. Exiting iterative step."
            )
            break

    # Final training and saving model
    final_known_mask = df["CAUSE_CLASS"].isin(["Human", "Natural"])
    pipeline = model(df, final_known_mask, params_path)
    # X_train, X_test, y_train, y_test = split_data(df[final_known_mask])
    # pipeline = model(params_path=params_path)
    # pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_save_path)
    # df.to_csv("data/interim/wildfire_clean_preassigned.csv", index=False)
    print("\nFinal model trained and saved.")


if __name__ == "__main__":
    iterative_labeling(
        data_path="data/interim/wildfire_clean.csv",
        model_save_path="models/best_lgbm_model.pkl",
        params_path="models/best_lgbm_params.pkl",
        threshold=0.95,
        max_iter=50,
        patience=1,
        # relative_threshold=0.05
    )
