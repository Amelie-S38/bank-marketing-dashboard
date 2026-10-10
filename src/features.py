"""Création des variables dérivées utilisées par l'analyse et le dashboard."""

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie de df avec les colonnes tranche_age, nb_appels et tranche_euribor."""
    df = df.copy()

    df["tranche_age"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 55, 65, 100],
        labels=["<25", "25-34", "35-44", "45-54", "55-64", "65+"],
        right=False,
    )

    # 6 signifie "6 appels et plus"
    df["nb_appels"] = df["campaign"].clip(upper=6)

    df["tranche_euribor"] = pd.cut(
        df["euribor3m"],
        bins=[0, 1, 2, 10],
        labels=["<1", "1-2", "2+"],
        right=False,
    )

    return df