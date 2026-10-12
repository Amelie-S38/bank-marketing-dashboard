"""Graphiques Plotly du dashboard."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Palette : modifier ici pour changer l'apparence de tous les graphiques
HAUT, BAS = "Au-dessus de la moyenne", "Sous la moyenne"
COULEURS = {HAUT: "#00C2A8", BAS: "#3D4F6B"}
COULEUR_MOYENNE = "#F2B84B"
COULEUR_LIGNE = "#8FA3BF"
COULEUR_TEXTE = "#E6EDF3"
COULEUR_GRILLE = "rgba(255,255,255,0.08)"


def _preparer(res, moyenne):
    """Ajoute une colonne indiquant si le taux est au-dessus ou sous la moyenne."""
    res = res.copy()
    res["position"] = res["taux"].apply(lambda t: HAUT if t >= moyenne else BAS)
    return res


def _texte_moyenne(moyenne):
    return f"Moyenne : {moyenne:.1f} %".replace(".", ",")


def _ligne_moyenne_h(fig, moyenne):
    """Ligne horizontale de moyenne, avec une pastille lisible."""
    fig.add_hline(
        y=moyenne,
        line_dash="dash",
        line_color=COULEUR_MOYENNE,
        annotation_text=_texte_moyenne(moyenne),
        annotation_position="top right",
        annotation_font=dict(color="#0E1117", size=12),
        annotation_bgcolor=COULEUR_MOYENNE,
    )


def _finaliser(fig):
    """Réglages communs : fond transparent, grille discrète, pas de légende."""
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COULEUR_TEXTE),
        margin=dict(t=60),
    )
    fig.update_xaxes(gridcolor=COULEUR_GRILLE, zeroline=False)
    fig.update_yaxes(gridcolor=COULEUR_GRILLE, zeroline=False)
    return fig


def graphique_taux(res, colonne, titre, moyenne):
    """Barres verticales du taux par segment, avec la moyenne en pointillés."""
    fig = px.bar(
        _preparer(res, moyenne),
        x=colonne,
        y="taux",
        text="taux",
        color="position",
        color_discrete_map=COULEURS,
        hover_data=["appels"],
        title=titre,
        labels={"taux": "Taux de souscription (%)", colonne: ""},
    )
    fig.update_traces(
        texttemplate="%{text} %",
        textposition="outside",
        textfont=dict(color=COULEUR_TEXTE),
        marker_line_width=0,
    )
    _ligne_moyenne_h(fig, moyenne)
    fig.update_xaxes(type="category")
    fig.update_layout(bargap=0.3)
    return _finaliser(fig)


def graphique_taux_horizontal(res, colonne, titre, moyenne):
    """Barres horizontales triées, pour les variables à nombreuses modalités."""
    fig = px.bar(
        _preparer(res.sort_values("taux"), moyenne),
        x="taux",
        y=colonne,
        orientation="h",
        text="taux",
        color="position",
        color_discrete_map=COULEURS,
        hover_data=["appels"],
        title=titre,
        labels={"taux": "Taux de souscription (%)", colonne: ""},
    )
    fig.update_traces(
        texttemplate="%{text} %",
        textposition="outside",
        textfont=dict(color=COULEUR_TEXTE),
        marker_line_width=0,
    )
    fig.add_vline(
        x=moyenne,
        line_dash="dash",
        line_color=COULEUR_MOYENNE,
        annotation_text=_texte_moyenne(moyenne),
        annotation_position="bottom right",
        annotation_font=dict(color="#0E1117", size=12),
        annotation_bgcolor=COULEUR_MOYENNE,
    )
    fig.update_layout(bargap=0.3)
    return _finaliser(fig)


def graphique_courbe(res, colonne, titre, moyenne, titre_x=""):
    """Courbe du taux pour un axe ordonné. Chaque point est coloré selon la moyenne.

    Les étiquettes sont placées au-dessus du point quand le taux est au-dessus de la moyenne,
    en dessous sinon, pour éviter qu'elles ne chevauchent la ligne de moyenne.
    """
    res = _preparer(res, moyenne)
    fig = px.line(
        res,
        x=colonne,
        y="taux",
        markers=True,
        text="taux",
        hover_data=["appels"],
        title=titre,
        labels={"taux": "Taux de souscription (%)", colonne: titre_x},
    )
    positions_texte = [
        "top center" if t >= moyenne else "bottom center" for t in res["taux"]
    ]
    fig.update_traces(
        line=dict(color=COULEUR_LIGNE, width=3),
        marker=dict(
            size=14,
            color=res["position"].map(COULEURS).tolist(),
            line=dict(width=2, color="#0E1117"),
        ),
        texttemplate="%{text} %",
        textposition=positions_texte,
        textfont=dict(color=COULEUR_TEXTE),
    )
    _ligne_moyenne_h(fig, moyenne)
    fig.update_xaxes(type="category")
    fig = _finaliser(fig)
    fig.update_yaxes(rangemode="tozero")
    return fig


def graphique_volume_taux(res, colonne, titre):
    """Barres = nombre d'appels (axe gauche), courbe = taux de souscription (axe droit)."""
    x = res[colonne].astype(str)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=x,
            y=res["appels"],
            name="Nombre d'appels",
            marker_color=COULEURS[BAS],
            opacity=0.9,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=res["taux"],
            name="Taux de souscription (%)",
            mode="lines+markers+text",
            text=[f"{t} %" for t in res["taux"]],
            textposition="top center",
            textfont=dict(color=COULEUR_TEXTE),
            line=dict(color=COULEURS[HAUT], width=3),
            marker=dict(size=12, color=COULEURS[HAUT]),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title=titre,
        showlegend=True,
        legend=dict(orientation="h", y=-0.15),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COULEUR_TEXTE),
        margin=dict(t=60),
    )
    fig.update_xaxes(type="category", gridcolor=COULEUR_GRILLE)
    fig.update_yaxes(title_text="Nombre d'appels", gridcolor=COULEUR_GRILLE, secondary_y=False)
    # Axe de droite : graduations rondes (0, 10, 20...) pour rester lisible
    fig.update_yaxes(
        title_text="Taux de souscription (%)",
        range=[0, 60],
        dtick=10,
        showgrid=False,
        secondary_y=True,
    )
    return fig