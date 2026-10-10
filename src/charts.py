"""Graphiques Plotly du dashboard."""

import plotly.express as px


def graphique_taux(res, colonne, titre, moyenne):
    """Diagramme en barres du taux par segment, avec la moyenne globale en pointillés."""
    fig = px.bar(
        res,
        x=colonne,
        y="taux",
        text="taux",
        hover_data=["appels"],
        title=titre,
        labels={"taux": "Taux de souscription (%)", colonne: ""},
    )
    fig.add_hline(y=moyenne, line_dash="dash", annotation_text="Moyenne globale")
    fig.update_traces(texttemplate="%{text} %", textposition="outside")
    return fig