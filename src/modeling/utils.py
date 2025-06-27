# src/modeling/utils.py
import logging
from src.utils import assign
from .training import model
# from .training import fit_model
# from .utils import split_data


def setup_logging(log_file: str = "logs/modeling.log", level: int = logging.INFO):
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def assign_trained(
    df,
    mask,
    *,
    value=None,
    encoder=None,
    params_path: str = "models/best_lgbm_params.pkl",
    num_assigned=False,
    threshold=0.95,
):
    """Reassingn data with trained model and return the data

    Args:
        df (_type_): _description_
        mask (_type_): _description_
        value (_type_, optional): _description_. Defaults to None.
        encoder (_type_, optional): _description_. Defaults to None.
        params_path (str, optional): _description_. Defaults to "models/best_lgbm_params.pkl".
        num_assigned (bool, optional): _description_. Defaults to False.
        threshold (float, optional): _description_. Defaults to 0.95.

    Returns:
        _type_: _description_
    """
    pipeline = model(df, mask, params_path)

    if num_assigned:
        return assign(
            df, df[~mask], pipeline, value, encoder, as_list=True, threshold=threshold
        )

    else:
        return assign(df, df[~mask], pipeline, value, encoder, threshold=threshold)
