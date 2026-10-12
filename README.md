# Campagne de marketing bancaire : qui souscrit à un dépôt à terme ?

Dashboard interactif (Python, pandas, Plotly, Streamlit) qui analyse 41 172 appels de télémarketing d'une banque portugaise pour répondre à une question : **quels profils de clients souscrivent le plus, et comment cibler plus efficacement les prochains appels ?**

**[Voir le dashboard en ligne](LIEN_STREAMLIT_A_AJOUTER)**

![Aperçu du dashboard](images/dashboard.png)

## Enseignements clés

Le taux de souscription global est de **11,3 %**.

| Axe | Segment le plus réceptif | Taux | Segment le moins réceptif | Taux |
|---|---|---|---|---|
| Historique | Clients ayant déjà souscrit lors d'une campagne précédente | 65,1 % | Clients jamais contactés | 8,8 % |
| Âge | 65 ans et plus | 47,3 % | 45-54 ans | 8,6 % |
| Métier | Étudiants | 31,4 % | Ouvriers (blue-collar) | 6,9 % |
| Contexte (Euribor 3 mois) | Moins de 1 % | 45,7 % | 2 % et plus | 4,8 % |
| Effort commercial | 1 appel | 13,0 % | 6 appels et plus | 5,5 % |

- La campagne a surtout appelé des clients peu réceptifs : 86 % des appels visaient des clients jamais contactés.
- Les 35-54 ans concentrent plus de la moitié des appels pour un taux inférieur à la moyenne.
- Insister auprès d'un même client est peu rentable : le taux baisse à chaque appel supplémentaire.

## Données

- **Source** : jeu de données *Bank Marketing* de l'UCI Machine Learning Repository, fichier `bank-additional-full.csv` (41 188 appels, 21 variables), licence CC BY 4.0.
- **Référence** : Moro, S., Cortez, P., Rita, P. (2014). *A data-driven approach to predict the success of bank telemarketing*. Decision Support Systems.

## Méthode

Le détail, avec les justifications, est dans les notebooks.

- **Nettoyage** (`notebooks/01_exploration.ipynb`) :
  - 12 doublons et 4 appels de durée nulle supprimés (41 188 → 41 172 lignes) ;
  - code `999` de `pdays` (« jamais contacté » ou délai inconnu) remplacé par une valeur manquante ;
  - valeurs `unknown` conservées comme modalité à part, après avoir vérifié que leur comportement le justifie ;
  - colonnes renommées (points remplacés par des underscores) et variable cible `y` convertie en 0/1.
- **Analyse** (`notebooks/02_analyse.ipynb`) : taux de souscription et volume d'appels par segment (historique, âge, métier, nombre d'appels, Euribor).
- **Année reconstituée** : le fichier ne contient pas l'année des appels. Elle est déduite de l'ordre chronologique des lignes (mai 2008 à novembre 2010). Cette reconstitution est cohérente avec l'évolution de l'Euribor (4,82 en 2008, 1,23 en 2009, 0,81 en 2010), mais il s’agit d’une déduction et non d’une donnée d’origine.

## Limites

- Les résultats décrivent des **associations**, pas des causes.
- L'année et l'Euribor sont **confondus** : on ne peut pas séparer l'effet du contexte économique de celui de la stratégie d'appel de la banque.
- La campagne ne couvre que 10 mois sur 12 (pas de janvier ni février).
- La durée de l'appel (`duration`) est exclue de l'analyse : elle n'est connue qu'après l'appel et ne peut pas servir au ciblage.
- Certains segments sont de petite taille : le volume est indiqué au survol de chaque graphique.

## Installation

```bash
git clone https://github.com/Amelie-S38/bank-marketing-dashboard.git
cd bank-marketing-dashboard
python -m venv venv
venv\Scripts\activate        # Windows (source venv/bin/activate sur Mac/Linux)
pip install -r requirements.txt
streamlit run app.py
```

## Structure du projet

```
bank-marketing-dashboard/
├── app.py                  # dashboard Streamlit (mise en page, filtres)
├── src/
│   ├── features.py         # colonnes dérivées (tranches d'âge, Euribor, année...)
│   ├── analysis.py         # calcul des taux par segment
│   └── charts.py           # graphiques Plotly
├── notebooks/
│   ├── 01_exploration.ipynb   # diagnostic et nettoyage
│   └── 02_analyse.ipynb       # analyse et choix des indicateurs
├── data/
│   ├── raw/                # données brutes (jamais modifiées)
│   └── processed/          # données nettoyées
├── images/                 # captures d'écran
└── requirements.txt
```

## Auteure

**Amélie Silvestre**, freelance data analyst.
Projet réalisé dans le cadre de mon portfolio : [mon profil Malt](https://www.malt.fr/profile/ameliesilvestre?origin=dashboard_profile_name) · [GitHub](https://github.com/Amelie-S38)