from typing import Union



def fix_assign(df):
    df.loc[
        (df.CAUSE == "Unspecified causes") & (df.CAUSE_CLASS == "Human"), "CAUSE"
    ] = "Human but unspecified causes"
    df.loc[df.CAUSE_CLASS == "Natural", "CAUSE"] = "Natural"
    return df


def assign(
    df,
    sample,
    estimator,
    value: Union[dict, str, float] = ...,
    encoder: ... = None,
    y="CAUSE_CLASS",
    threshold=0.9,
    verbose=0,
    as_list=False,
):
    """Confidently reassign labels and return the new data

    Args:
        df (_type_): _description_
        sample (_type_): _description_
        estimator (_type_): _description_
        value (_type_, optional): _description_. Defaults to None.
        encoder (_type_, optional): _description_. Defaults to None.
        y (str, optional): _description_. Defaults to "CAUSE_CLASS".
        threshold (float, optional): _description_. Defaults to 0.9.
        verbose (int, optional): _description_. Defaults to 0.
        as_list (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    # df = dfs.copy()
    features = ["FIRE_SIZE", "LATITUDE", "LONGITUDE"]

    probs = estimator.predict_proba(sample[features])

    max_probs = probs.max(axis=1)
    classes = probs.argmax(axis=1)

    # print(max(max_probs), "THE MAX GUY AH")
    mask = max_probs >= threshold

    num_assigned = mask.sum()
    if verbose >= 0:
        print(f"Reassigned {num_assigned} labeel")

    if isinstance(value, dict):
        pred_labels = [encoder[i] for i in classes[mask]]
        # pred_labels = ["Human" if i == 1 else "Natural" for i in classes[mask]]
    elif value is Ellipsis and encoder is not None:
        pred_labels = encoder.inverse_transform(classes[mask])
    else:
        pred_labels = [value if i == 1 else "Unknown" for i in classes[mask]]

    # print(pred_labels, len(pred_labels))
    # import numpy as np; print(np.unique(pred_labels));
    df.loc[sample.index[mask], y] = pred_labels
    df = fix_assign(df)
    return [df, num_assigned] if as_list else df
    # return df
