"""Création des variables dérivées utilisées par l'analyse et le dashboard."""

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie de df avec les colonnes tranche_age, nb_appels, tranche_euribor et annee."""
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
        labels=["Moins de 1 %", "Entre 1 et 2 %", "2 % et plus"],
        right=False,
    )
    # L'année n'existe pas dans le fichier : on la déduit de l'ordre chronologique des lignes
    # (le mois "recule" quand on passe à l'année suivante). Données : mai 2008 à novembre 2010
    mois_num = df["month"].map({
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    })
    df["annee"] = 2008 + (mois_num.diff() < 0).cumsum()

    return df