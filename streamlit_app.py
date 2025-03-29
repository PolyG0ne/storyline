import streamlit as st
import pandas as pd
import time

# Configuration de la page
st.set_page_config(layout="wide", page_title="Timeline 1980-2030")

# Utilisation du système de thème de Streamlit (disponible dans les versions récentes)
st.markdown("""
<style>
    /* Styles personnalisés qui respectent le thème Streamlit */
    .timeline-container {
        position: fixed;
        left: 2rem;
        top: 50%;
        transform: translateY(-50%);
        background: var(--background-color);
        box-shadow: 0 0 15px var(--shadow-color);
        padding: 20px 0;
        border-radius: 10px;
        z-index: 1000;
        width: 100px;
        text-align: center;
    }
    
    .year-slot {
        margin: 15px 0;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    
    .year-current {
        font-weight: bold;
        font-size: 24px;
        color: var(--primary-color);
    }
    
    .year-above, .year-below {
        opacity: 0.7;
    }
    
    .year-far {
        opacity: 0.4;
    }
    
    .year-edge {
        opacity: 0.2;
    }
    
    .main-content {
        margin-left: 120px;
    }
    
    .timeline-fade {
        position: absolute;
        left: 0;
        width: 100%;
        height: 30px;
        pointer-events: none;
    }
    
    .timeline-fade-top {
        top: 0;
        background: linear-gradient(to bottom, 
                    var(--background-color) 0%, 
                    transparent 100%);
    }
    
    .timeline-fade-bottom {
        bottom: 0;
        background: linear-gradient(to top, 
                    var(--background-color) 0%, 
                    transparent 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'current_year_index' not in st.session_state:
    st.session_state.current_year_index = 0
    st.session_state.visible_sections = set()

# Années à afficher (de 1980 à 2030 par intervalles de 2 ans)
years = list(range(1980, 2031, 2))

# Fonction pour générer la timeline en HTML
def generate_timeline_html(years, current_index):
    timeline_html = '<div class="timeline-container">'
    timeline_html += '<div class="timeline-fade timeline-fade-top"></div>'
    
    # Afficher 5 années: 2 au-dessus, l'année courante, et 2 en-dessous
    for i in range(max(0, current_index-2), min(len(years), current_index+3)):
        if i == current_index:
            class_name = "year-slot year-current"
        elif i == current_index-1 or i == current_index+1:
            class_name = "year-slot year-above" if i < current_index else "year-slot year-below"
        elif i == current_index-2 or i == current_index+2:
            class_name = "year-slot year-far"
        else:
            class_name = "year-slot year-edge"
        
        timeline_html += f'<div class="{class_name}">{years[i]}</div>'
    
    timeline_html += '<div class="timeline-fade timeline-fade-bottom"></div>'
    timeline_html += '</div>'
    return timeline_html

# Création de la structure de l'application
# Utilisation du conteneur pour le timeline fixe
timeline_container = st.container()

# Création de deux colonnes: une invisible pour l'espace et une pour le contenu principal
main_container = st.container()
with main_container:
    _, main_col = st.columns([1, 4])

# Fonction callback pour mettre à jour l'année courante
def update_current_year(year_index):
    st.session_state.current_year_index = year_index
    st.experimental_rerun()

# Créer des sections pour chaque année
with main_col:
    st.header("Contenu principal")
    st.write("Faites défiler la page pour voir la ligne temporelle se déplacer comme une roue du temps.")
    
    # Créer un contenu suffisamment long pour permettre le défilement
    for i, year in enumerate(years):
        # Utilisation de l'API moderne de Streamlit pour la détection de visibilité
        with st.expander(f"Année {year}", expanded=True):
            st.subheader(f"Section de l'année {year}")
            st.write(f"Contenu pour l'année {year}. Continuez à défiler pour voir l'effet de 'machine à sous' sur la ligne temporelle.")
            
            # Ajouter du contenu factice pour chaque année
            st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate eu pharetra nec, mattis ac neque.")
            st.write("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
            
            # Bouton invisible qui agit comme un "trigger" quand la section est visible
            # Cette technique évite d'utiliser du JavaScript injecté
            trigger = st.button(
                "Visible", 
                key=f"trigger_{i}", 
                help="Élément de détection de visibilité",
                on_click=update_current_year,
                args=(i,),
                use_container_width=True
            )
            
            # Utiliser CSS pour masquer le bouton tout en le gardant fonctionnel
            st.markdown(f"""
            <style>
            div[data-testid="stButton"] button[kind="secondary"][aria-describedby="help-trigger_{i}"] {{
                visibility: hidden;
                height: 1px;
                position: sticky;
                top: 50vh;
                z-index: 0;
            }}
            </style>
            """, unsafe_allow_html=True)

# Afficher la timeline dans le conteneur fixe
with timeline_container:
    st.markdown(generate_timeline_html(years, st.session_state.current_year_index), unsafe_allow_html=True)

# Utiliser les fonctions de métriques de Streamlit pour afficher des informations supplémentaires
with st.sidebar:
    st.title("Informations")
    st.metric("Année courante", years[st.session_state.current_year_index])
    
    # Ajout d'un sélecteur d'année pour permettre une navigation rapide
    selected_year = st.select_slider(
        "Naviguer rapidement",
        options=years,
        value=years[st.session_state.current_year_index]
    )
    
    # Si l'année sélectionnée change, mettre à jour l'index
    if selected_year != years[st.session_state.current_year_index]:
        update_current_year(years.index(selected_year))