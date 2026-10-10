"""Calculs de taux de souscription par segment."""

import pandas as pd


def taux_par(df, colonne, ordre=None):
    """Taux de souscription (%) et nombre d'appels par modalité de `colonne`."""
    res = df.groupby(colonne, observed=True)["y"].agg(taux="mean", appels="count").reset_index()
    res["taux"] = (res["taux"] * 100).round(1)
    if ordre:
        res[colonne] = pd.Categorical(res[colonne], categories=ordre, ordered=True)
        res = res.sort_values(colonne)
    return res