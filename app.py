import pandas as pd
import streamlit as st

from src.analysis import taux_par
from src.charts import (
    BAS,
    COULEUR_MOYENNE,
    COULEURS,
    HAUT,
    graphique_courbe,
    graphique_taux,
    graphique_taux_horizontal,
    graphique_volume_taux,
)
from src.features import add_features

st.set_page_config(page_title="Campagne bancaire", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {font-size: 2.8rem; font-weight: 700; color: #00C2A8;}
    [data-testid="stMetricLabel"] {font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/bank_marketing_clean.csv")
    return add_features(df)


def fmt(n):
    return f"{n:,}".replace(",", " ")


ORDRE_AGE = ["<25", "25-34", "35-44", "45-54", "55-64", "65+"]
ORDRE_EURIBOR = ["Moins de 1 %", "Entre 1 et 2 %", "2 % et plus"]

df_all = load_data()
taux_global = df_all["y"].mean() * 100

# --- Barre latérale ---
ORDRE_MOIS = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
NOMS_MOIS = {
    "mar": "Mars", "apr": "Avril", "may": "Mai", "jun": "Juin", "jul": "Juillet",
    "aug": "Août", "sep": "Septembre", "oct": "Octobre", "nov": "Novembre", "dec": "Décembre",
}

st.sidebar.header("Filtres")

annees = sorted(df_all["annee"].unique())
choix_annees = st.sidebar.multiselect("Année(s)", annees, default=annees)

# On ne propose que les mois qui existent pour les années choisies
mois_dispos = [m for m in ORDRE_MOIS if m in df_all[df_all["annee"].isin(choix_annees)]["month"].unique()]
choix_mois = st.sidebar.multiselect(
    "Mois", mois_dispos, default=mois_dispos, format_func=lambda m: NOMS_MOIS[m]
)

st.sidebar.caption(
    "L'année n'est pas dans le fichier d'origine : elle est déduite de l'ordre chronologique des lignes "
    "(campagne de mai 2008 à novembre 2010). Aucun appel en janvier ni février."
)

if not choix_annees or not choix_mois:
    st.warning("Sélectionne au moins une année et un mois dans la barre latérale.")
    st.stop()

df = df_all[df_all["annee"].isin(choix_annees) & df_all["month"].isin(choix_mois)]
moyenne = df["y"].mean() * 100
moyenne_txt = f"{moyenne:.1f}".replace(".", ",")

# --- En-tête et KPI ---
st.title("Campagne de marketing bancaire")
st.caption("Qui souscrit à un dépôt à terme, et comment mieux cibler les appels ?")
st.caption("Taux de souscription = part des clients appelés qui ont souscrit un dépôt à terme.")

delta = None
if len(df) < len(df_all):
    delta = f"{moyenne - taux_global:+.1f} pt vs ensemble".replace(".", ",")

c1, c2, c3 = st.columns(3)
c1.metric("Appels", fmt(len(df)), border=True)
c2.metric("Souscriptions", fmt(int(df["y"].sum())), border=True)
c3.metric("Taux de souscription", f"{moyenne_txt} %", delta=delta, border=True)

st.divider()

# --- Légende partagée ---
st.markdown(
    f"""
    <div style="display:flex; gap:28px; flex-wrap:wrap; align-items:center; margin-bottom:8px;">
        <span><span style="display:inline-block;width:14px;height:14px;background:{COULEURS[HAUT]};border-radius:3px;margin-right:8px;vertical-align:middle;"></span>Taux supérieur à la moyenne</span>
        <span><span style="display:inline-block;width:14px;height:14px;background:{COULEURS[BAS]};border-radius:3px;margin-right:8px;vertical-align:middle;"></span>Taux inférieur à la moyenne</span>
        <span><span style="display:inline-block;width:22px;border-top:2px dashed {COULEUR_MOYENNE};margin-right:8px;vertical-align:middle;"></span>Moyenne de la sélection ({moyenne_txt} %)</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Graphiques ---
col_a, col_b = st.columns(2)
with col_a:
    res = taux_par(df, "poutcome")
    st.plotly_chart(
        graphique_taux(
            res, "poutcome",
            "Taux de souscription selon le résultat de la campagne précédente", moyenne,
        ),
        use_container_width=True,
    )
with col_b:
    res = taux_par(df, "tranche_age", ordre=ORDRE_AGE)
    st.plotly_chart(
        graphique_courbe(
            res, "tranche_age",
            "Taux de souscription selon la tranche d'âge", moyenne,
            titre_x="Tranche d'âge du client (années)",
        ),
        use_container_width=True,
    )

res = taux_par(df, "job")
st.plotly_chart(
    graphique_taux_horizontal(res, "job", "Taux de souscription selon le métier", moyenne),
    use_container_width=True,
)

col_c, col_d = st.columns(2)
with col_c:
    res = taux_par(df, "nb_appels")
    st.plotly_chart(
        graphique_courbe(
            res, "nb_appels",
            "Taux de souscription selon le nombre d'appels au client", moyenne,
            titre_x="Nombre d'appels au même client (6 = 6 et plus)",
        ),
        use_container_width=True,
    )
with col_d:
    res = taux_par(df, "tranche_euribor", ordre=ORDRE_EURIBOR)
    st.plotly_chart(
        graphique_courbe(
            res, "tranche_euribor",
            "Taux de souscription selon l'Euribor 3 mois", moyenne,
            titre_x="Niveau de l'Euribor 3 mois au moment de l'appel",
        ),
        use_container_width=True,
    )
    st.caption(
        "L'Euribor est le taux d'intérêt de référence entre banques. Il décrit le contexte "
        "économique au moment de l'appel, pas une caractéristique du client."
    )

# --- Volume et taux par année ---
st.subheader("Où l'effort commercial a-t-il été concentré ?")
st.caption(
    "Les barres montrent le nombre d'appels, la courbe le taux de souscription. "
    "La banque a appelé massivement quand le taux était le plus faible."
)
res = taux_par(df, "annee")
st.plotly_chart(
    graphique_volume_taux(res, "annee", "Appels et taux de souscription par année"),
    use_container_width=True,
)