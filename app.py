import pandas as pd
import streamlit as st

from src.analysis import taux_par
from src.charts import graphique_taux
from src.features import add_features

st.set_page_config(page_title="Campagne bancaire", page_icon="🏦", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/bank_marketing_clean.csv")
    return add_features(df)


df = load_data()
moyenne = df["y"].mean() * 100

st.title("Campagne de marketing bancaire")
st.caption("Qui souscrit à un dépôt à terme, et comment mieux cibler les appels ?")

col1, col2, col3 = st.columns(3)
col1.metric("Appels", f"{len(df):,}".replace(",", " "))
col2.metric("Souscriptions", f"{df['y'].sum():,}".replace(",", " "))
col3.metric("Taux de souscription", f"{moyenne:.1f} %".replace(".", ","))

st.divider()
col_a, col_b = st.columns(2)

with col_a:
    res = taux_par(df, "poutcome")
    st.plotly_chart(
        graphique_taux(res, "poutcome", "Taux selon l'historique avec la banque", moyenne),
        use_container_width=True,
    )

with col_b:
    res = taux_par(df, "tranche_age", ordre=["<25", "25-34", "35-44", "45-54", "55-64", "65+"])
    st.plotly_chart(
        graphique_taux(res, "tranche_age", "Taux selon la tranche d'âge", moyenne),
        use_container_width=True,
    )