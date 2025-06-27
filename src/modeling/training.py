# src/modeling/pipeline.py
import joblib
from pycaret.classification import *
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDClassifier
from pandas import DataFrame
from src.preprocessing.utils import split_data


def model(
    X: DataFrame,
    mask=None,
    class_type="binary",
    y: str = "CAUSE_CLASS",
    params_path: str = "models/best_lgbm_params.pkl",
    random_state: int = 37,
    n_sample: int = None,
):
    """Split, train and return the model

    Args:
        X (DataFrame, optional): _description_. Defaults to None.
        class_type (str, optional): _description_. Defaults to "binary".
        y (str, optional): _description_. Defaults to "CAUSE_CLASS".
        params_path (str, optional): _description_. Defaults to "models/best_lgbm_params.pkl".
        random_state (int, optional): _description_. Defaults to 37.

    Returns:
        _type_: _description_
    """
    # Load the best hyperparameters
    X = X if mask is None else X[mask]
    X = X.sample(n=n_sample, random_state=random_state) if n_sample is not None else X
    # if objective even exists
    if class_type == "multiclass":
        # if num_class is None:
        # raise ValueError("For multiclass classification, please specify num_class")
        # best_params["objective"] = "multiclass"
        # best_params["num_class"] = num_class

        model = setup(
            data=X[["FIRE_SIZE", "LATITUDE", "LONGITUDE", "CAUSE"]],
            target=y,
            session_id=random_state,
            fold=2,
            normalize=True,
            remove_multicollinearity=True,
            feature_selection=True,
        )

        best_model = compare_models(sort="F1")

        return finalize_model(tune_model(best_model, optimize="F1"))

    best_params = {
        # key.replace("clf__", ""): val for key, val in joblib.load(params_path).items()
        key.split("__", 1)[1]: val
        for key, val in joblib.load(params_path).items()
        if "__" in key
    }

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "clf",
                SGDClassifier(**best_params, random_state=random_state, verbose=0)
                if params_path == "models/best_sgd_params.json"
                else lgb.LGBMClassifier(
                    **best_params, random_state=random_state, verbose=-1
                ) if params_path == "models/best_lgb_params.json"
                else KMeans(
                    **best_params, random_state=random_state, verbose=0
                )
            ),
        ]
    )

    X_train, X_test, y_train, y_test = split_data(X)
    # pipeline = model(params_path=params_path)
    model.fit(X_train, y_train)

    return model
