import streamlit as st
import random
import pandas as pd
import altair as alt

# Configuration de la page
st.set_page_config(page_title="Timeline Verticale", layout="wide")

# Titre de l'application
st.title("Timeline Verticale (1980-2030)")

# Génération des années avec variation aléatoire
def generer_annees():
    annees = []
    annee_courante = 1980
    
    while annee_courante <= 2030:
        annees.append(annee_courante)
        # Variation aléatoire entre 1 et 5 ans
        variation = random.randint(1, 5)
        annee_courante += variation
    
    return annees

# Création du dataframe pour la visualisation
def creer_dataframe(annees):
    return pd.DataFrame({
        'annee': annees,
        'position': range(len(annees))
    })

# Création de la timeline
def creer_timeline(df):
    # Création du graphique de base
    timeline = alt.Chart(df).mark_rule(
        strokeWidth=2
    ).encode(
        y=alt.Y('position:Q', axis=None)
    ).properties(
        width=10,
        height=600
    )
    
    # Ajout des années (gros chiffres)
    texte = alt.Chart(df).mark_text(
        fontSize=24,
        fontWeight='bold',
        align='left',
        dx=15
    ).encode(
        y=alt.Y('position:Q'),
        text='annee:N'
    )
    
    # Ajout des lignes horizontales (règle)
    lignes = alt.Chart(df).mark_rule(
        strokeWidth=1,
        strokeDash=[2, 2]
    ).encode(
        y=alt.Y('position:Q'),
        x=alt.value(0),
        x2=alt.value(300)
    )
    
    return (timeline + texte + lignes)

# Exécution principale
annees = generer_annees()
df = creer_dataframe(annees)

# Affichage de la timeline
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.altair_chart(creer_timeline(df), use_container_width=True)

# Information sur les années générées
st.sidebar.header("Informations")
st.sidebar.write(f"Nombre d'années affichées: {len(annees)}")
st.sidebar.write("Années sélectionnées:")
st.sidebar.write(annees)

# Option pour regénérer la timeline
if st.sidebar.button("Regénérer la timeline"):
    st.rerun()