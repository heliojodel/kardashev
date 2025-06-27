from dython.nominal import associations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_wildfire_distr(fire_sizes):
    fig = plt.figure(figsize=(10, 6))

    ax1 = fig.add_subplot(1, 2, 1)
    sns.stripplot(x=fire_sizes, ax=ax1)
    ax1.set_title("Fire Size Distribution")
    ax1.set_xlabel("Count")

    ax2 = fig.add_subplot(1, 2, 2)
    sns.boxplot(x=np.log(fire_sizes), ax=ax2)
    ax2.set_title("Log-Transformed Fire Sizes")
    ax2.set_xlabel("Count")

    plt.tight_layout()
    plt.show()


def plot_missing_values(df):
    plt.figure(figsize=(12, 6))
    plt.title("Missing Values")
    sns.heatmap(df.isnull(), cbar=False, annot=False, cmap="seismic")


def plot_causes_distr(causes, classes, latitude, longitude):
    _, ax = plt.subplots(2, 1, figsize=(10, 10))

    data = classes.value_counts()
    ax[0].bar(data.index, data.values, color=["r", "b", "g"][::-1])
    ax[0].set_title("Cause Class Distribution")
    ax[0].set_xlabel("Cause Class")
    ax[0].set_ylabel("Count")
    order = (
        pd.DataFrame({1: classes, 0: causes})
        .groupby([1, 0], observed=True)
        .size()
        .sort_values()
        .sort_index(level=1, ascending=[True])
    )

    sns.countplot(
        x=causes,
        hue=classes,
        order=order[order != 0].index.get_level_values(0),
        ax=ax[1],
        palette="dark:c",
    )
    ax[1].set_title("Cause Counts by Class")
    ax[1].set_xlabel("Cause")
    ax[1].set_ylabel("Count")
    ax[1].tick_params(axis="x", rotation=85)
    ax[1].legend(title="Cause Class")

    g = sns.JointGrid(x=longitude, y=latitude, hue=classes)
    g.figure.set_size_inches(10, 7)
    g.ax_joint.set_xlim(-180, -60)
    g.ax_joint.set_ylim(15, 75)

    sns.scatterplot(
        x=longitude,
        y=latitude,
        hue=classes,
        alpha=0.5,
        ax=g.ax_joint,
    )

    sns.kdeplot(
        y=latitude, ax=g.ax_marg_y, color="#ff817f", lw=2, bw_adjust=3.5, fill=True
    )

    sns.histplot(
        x=longitude,
        bins=25,
        color=(253 / 255, 54 / 255, 51 / 255) + (0.8,),
        ax=g.ax_marg_x,
        alpha=0.5,
    )


def plot_class_events(df, classes):
    if classes == "Natural":
        from sklearn.preprocessing import MinMaxScaler

        x = pd.to_datetime(
            df[df.NWCG_CAUSE_CLASSIFICATION == "Natural"]["DISCOVERY_DATE"]
        )
        dmonths = x.dt.month
        counts = dmonths.value_counts().sort_index()
        scaled_dmonths = MinMaxScaler(feature_range=(0, 0.5)).fit_transform(
            counts.values.reshape(-1, 1)
        )
        scaled_series = pd.Series(scaled_dmonths.flatten(), index=counts.index)

        _, ax = plt.subplots(figsize=(10, 6))
        scaled_series.plot(
            kind="bar", color="gray", alpha=0.5, label="Event Count", zorder=1, ax=ax
        )

        sns.kdeplot(
            dmonths,
            color="red",
            lw=2,
            bw_adjust=5,
            clip=(dmonths.min(), dmonths.max()),
            label="KDE",
            zorder=2,
            ax=ax,
        )
        ax.set_xlabel("Month")
        ax.set_ylabel("Density")

    if classes == "Human":
        y = pd.to_datetime(
            df[df.NWCG_CAUSE_CLASSIFICATION == "Human"]["DISCOVERY_TIME"],
            format="%H%M",
            errors="coerce",
        )
        hours = y.dt.hour
        hour_counts = hours.value_counts().sort_index()

        ax1 = plt.subplots(figsize=(10, 6))[1]
        ax2 = ax1.twinx()

        sns.ecdfplot(hours, ax=ax2, color="darkred", lw=2)
        ax2.set_ylabel("ECDF", color="darkred")
        ax2.tick_params(axis="y", labelcolor="darkred")

        hour_counts.plot(kind="bar", ax=ax1, color="skyblue", alpha=0.7, width=0.8)
        ax1.set_xlabel("Hour")
        ax1.set_ylabel("Count", color="skyblue")
        ax1.tick_params(axis="y", labelcolor="skyblue")


def plot_assoc_corr(df, cmap="coolwarm", annot=True, fmt=".1f", **kwargs):
    association_result = associations(df, compute_only=True)
    association_df = association_result["corr"]

    sns.clustermap(association_df, cmap=cmap, annot=annot, fmt=fmt, **kwargs)
