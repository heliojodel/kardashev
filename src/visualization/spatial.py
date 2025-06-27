import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from pyod.models.iforest import IForest


def plot_outlier_map(
    df,
    contamination=0.01,
    scale_features=True,
    figsize=(12, 7),
    cmap="bwr",
    title="Outlier Map",
):
    cols = [
        col
        for col in df.select_dtypes(include="number").columns.tolist()
        if col not in ["LONGITUDE", "LATITUDE"]
    ]
    mask = df.DURATION > 0

    gdf = gpd.GeoDataFrame(
        df[mask], geometry=gpd.points_from_xy(df[mask].LONGITUDE, df[mask].LATITUDE), crs=4326
    ).to_crs(epsg=3857)

    iso = IForest(contamination=contamination, random_state=37)
    predictions = iso.fit_predict(
        df.loc[mask, cols].apply(stats.zscore)
        if scale_features
        else df.loc[mask, cols]
    )

    _, ax = plt.subplots(figsize=figsize)
    gdf.plot(ax=ax, column=predictions, legend=True, alpha=0.5, cmap=cmap)
    ax.set_title(title)
