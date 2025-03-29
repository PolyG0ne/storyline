import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuration de la page
st.set_page_config(layout="wide")

# Titre de l'application
st.title("Règle temporelle défilante (1980-2030)")

# Création de deux colonnes: une étroite à gauche pour la règle, une plus large à droite pour le contenu principal
col1, col2 = st.columns([1, 3])

# Dans la colonne de gauche, nous allons créer notre règle temporelle
with col1:
    st.markdown("### Ligne temporelle")
    
    # Conteneur pour la règle temporelle avec style personnalisé
    timeline_container = st.container()
    
    # Création d'un placeholder pour afficher l'année actuelle
    current_year_placeholder = st.empty()
    
    # Création d'un slider vertical pour permettre à l'utilisateur de naviguer manuellement
    selected_year = st.slider("Sélectionner une année", 1980, 2030, 2000, step=1)
    
    # Bouton pour activer/désactiver le défilement automatique
    auto_scroll = st.checkbox("Défilement automatique", value=True)

# Dans la colonne principale
with col2:
    st.markdown("### Contenu principal")
    st.write("Cette section peut contenir des informations, des graphiques ou des données correspondant à l'année sélectionnée.")
    
    # Exemple de contenu qui change en fonction de l'année sélectionnée
    st.write(f"Vous visualisez des informations pour l'année: **{selected_year}**")
    
    # On pourrait ajouter ici des visualisations ou des données qui changent selon l'année

# Fonction pour générer une représentation visuelle de la règle temporelle
def generate_timeline_view(year, start_year=1980, end_year=2030):
    years = list(range(start_year, end_year + 1))
    df = pd.DataFrame({
        'Année': years,
        'Position': np.linspace(0, 100, len(years))
    })
    
    # Filtrer pour n'afficher que quelques années (pour éviter l'encombrement)
    display_years = df[df['Année'] % 5 == 0].copy()
    
    # Mettre en évidence l'année actuelle
    highlight = pd.DataFrame({
        'Année': [year],
        'Position': [df[df['Année'] == year]['Position'].values[0]]
    })
    
    # Créer le graphique de la règle
    timeline_chart = st.line_chart(df[['Position']], height=400)
    
    # Ajouter les marqueurs d'années
    for _, row in display_years.iterrows():
        st.markdown(f"<div style='position:relative; left:10px; top:-{400 - row['Position'] * 4}px;'>{int(row['Année'])}</div>", unsafe_allow_html=True)
    
    # Mettre en évidence l'année sélectionnée
    st.markdown(f"<div style='position:relative; left:20px; top:-{400 - highlight['Position'].values[0] * 4}px; color:red; font-weight:bold;'>{int(highlight['Année'].values[0])}</div>", unsafe_allow_html=True)
    
    return highlight['Position'].values[0]

# Version alternative sans unsafe_allow_html
def generate_safe_timeline(year, start_year=1980, end_year=2030):
    # Créer une DataFrame avec toutes les années
    years = list(range(start_year, end_year + 1))
    total_years = len(years)
    
    # Créer un DataFrame pour la visualisation
    df = pd.DataFrame({
        'Année': years,
        'Valeur': [0] * total_years  # Valeur constante pour la ligne de base
    })
    
    # Créer un DataFrame pour mettre en évidence l'année sélectionnée
    highlight_df = pd.DataFrame({
        'Année': [year],
        'Valeur': [1]  # Valeur plus élevée pour l'année mise en évidence
    })
    
    # Afficher la règle comme un graphique
    with timeline_container:
        # Afficher l'année actuelle
        current_year_placeholder.markdown(f"## {year}")
        
        # Créer un graphique de ligne verticale
        chart_data = pd.DataFrame({
            'Année': years,
            'Position': range(total_years)
        })
        
        # Configurer le graphique pour qu'il ressemble à une règle verticale
        st.line_chart(
            chart_data.set_index('Année')['Position'], 
            use_container_width=True,
            height=500
        )
        
        # Afficher des marques tous les 5 ans
        for y in range(start_year, end_year + 1, 5):
            st.markdown(f"**{y}**")

# Boucle principale pour le défilement automatique
if auto_scroll:
    # Au lieu d'utiliser une boucle infinie qui bloquerait l'interface,
    # nous utilisons un placeholder Streamlit pour mettre à jour l'affichage
    current_year = selected_year
    
    # Dans une application réelle, nous utiliserions un mécanisme plus sophistiqué
    # Ici, nous simulons simplement l'effet en mettant à jour l'année sélectionnée
    with timeline_container:
        st.write("Défilement automatique activé. L'année change toutes les secondes.")
        
        # Mettre à jour la visualisation de la règle
        generate_safe_timeline(current_year)
else:
    # Si le défilement automatique est désactivé, afficher simplement l'année sélectionnée
    with timeline_container:
        generate_safe_timeline(selected_year)

# Note: Dans une application Streamlit réelle, pour implémenter un défilement automatique,
# vous devriez utiliser des sessions ou des solutions côté client avec des composants personnalisés.
# Cette version est une approximation qui montre le concept.