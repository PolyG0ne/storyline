import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(layout="wide")

# Titre de l'application
st.title("Ligne temporelle 1980-2030")

# Création de deux colonnes: une pour la règle temporelle, une pour le contenu principal
timeline_col, main_col = st.columns([1, 3])

# Configuration du style pour rendre la barre de défilement visible
st.markdown("""
<style>
    section.main > div {
        max-height: 100vh;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)  # Ce unsafe_allow_html est nécessaire pour le CSS, mais n'affecte pas le contenu

# Fonction pour créer la règle temporelle
def create_timeline(start_year=1980, end_year=2030, interval=2):
    years = list(range(start_year, end_year + 1, interval))
    
    # Utilisation de Streamlit pour la règle temporelle (sans unsafe_allow_html)
    with timeline_col:
        st.markdown("### Années")
        for year in years:
            # Créer un conteneur pour chaque année
            year_container = st.container()
            year_container.markdown(f"**{year}**")
            # Ajouter un espace pour la séparation
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Contenu factice pour créer de l'espace et permettre le défilement
            st.markdown("##")

# Création de contenu factice pour la colonne principale (pour tester le défilement)
def create_dummy_content():
    with main_col:
        st.header("Contenu principal")
        st.write("Faites défiler la page pour voir la ligne temporelle complète.")
        
        # Ajout de contenu pour tester le défilement
        for i in range(20):
            st.markdown(f"### Section {i+1}")
            st.write("Contenu de test pour permettre le défilement de la page.")
            st.markdown("---")

# Alternative sans utiliser unsafe_allow_html pour les espaces
def create_timeline_alt(start_year=1980, end_year=2030, interval=2):
    years = list(range(start_year, end_year + 1, interval))
    
    with timeline_col:
        st.markdown("### Années")
        for year in years:
            st.markdown(f"**{year}**")
            # Utiliser des espaces vides pour créer de la séparation
            for _ in range(3):
                st.text(" ")

# Exécution des fonctions
create_timeline_alt()  # Version alternative sans unsafe_allow_html pour les espaces
create_dummy_content()

# Si vous souhaitez utiliser la version originale avec un peu plus d'espace:
# create_timeline()
# create_dummy_content()