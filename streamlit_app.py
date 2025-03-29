import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuration de la page
st.set_page_config(layout="wide")

# Titre de l'application
st.title("Ligne temporelle 1980-2030")

# Style CSS pour créer l'effet de défilement de machine à sous
st.markdown("""
<style>
    .timeline-container {
        position: fixed;
        left: 2rem;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(to bottom, 
                    rgba(255,255,255,1) 0%, 
                    rgba(255,255,255,0.8) 10%, 
                    rgba(255,255,255,0.8) 90%, 
                    rgba(255,255,255,1) 100%);
        padding: 20px 0;
        border-radius: 10px;
        z-index: 1000;
        width: 100px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    
    .year-slot {
        margin: 15px 0;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    
    .year-current {
        font-weight: bold;
        font-size: 24px;
        color: #1E88E5;
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
    
    /* Ajouter un effet de fondu en haut et en bas */
    .timeline-fade-top, .timeline-fade-bottom {
        position: fixed;
        left: 2rem;
        width: 100px;
        height: 50px;
        z-index: 1001;
        pointer-events: none;
    }
    
    .timeline-fade-top {
        top: calc(50% - 140px);
        background: linear-gradient(to bottom, 
                    rgba(255,255,255,1) 0%, 
                    rgba(255,255,255,0) 100%);
    }
    
    .timeline-fade-bottom {
        top: calc(50% + 90px);
        background: linear-gradient(to top, 
                    rgba(255,255,255,1) 0%, 
                    rgba(255,255,255,0) 100%);
    }
</style>
""", unsafe_allow_html=True)

# Création de deux colonnes: une invisible pour l'espace et une pour le contenu principal
_, main_col = st.columns([1, 4])

# Années à afficher (de 1980 à 2030 par intervalles de 2 ans)
years = list(range(1980, 2031, 2))

# Variable de session pour suivre l'année courante
if 'current_year_index' not in st.session_state:
    st.session_state.current_year_index = 0

# Fonction pour générer le HTML de la ligne temporelle
def generate_timeline_html(years, current_index):
    timeline_html = '<div class="timeline-container">'
    
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
    
    timeline_html += '</div>'
    
    # Ajouter les effets de fondu en haut et en bas
    timeline_html += '<div class="timeline-fade-top"></div>'
    timeline_html += '<div class="timeline-fade-bottom"></div>'
    
    return timeline_html

# Créer des sections pour chaque année
with main_col:
    st.header("Contenu principal")
    st.write("Faites défiler la page pour voir la ligne temporelle se déplacer comme une roue du temps.")
    
    # Créer un contenu suffisamment long pour permettre le défilement
    for i, year in enumerate(years):
        # Marquer la section avec un id pour la référencer plus tard
        st.markdown(f'<div id="year-section-{i}"></div>', unsafe_allow_html=True)
        
        st.subheader(f"Section de l'année {year}")
        st.write(f"Contenu pour l'année {year}. Continuez à défiler pour voir l'effet de 'machine à sous' sur la ligne temporelle.")
        
        # Ajouter du contenu factice pour chaque année
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate eu pharetra nec, mattis ac neque.")
        st.write("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        
        # Détection de la section visible
        js_code = f"""
        <script>
            // Cette fonction sera exécutée lorsque cette section sera visible
            const observer{i} = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            value: {i}
                        }}, '*');
                    }}
                }});
            }}, {{ threshold: 0.5 }});
            
            // Observer cette section
            observer{i}.observe(document.getElementById('year-section-{i}'));
        </script>
        """
        st.markdown(js_code, unsafe_allow_html=True)
        
        # Ajouter un séparateur
        st.markdown("---")

# Afficher la ligne temporelle (fixe sur le côté gauche)
st.markdown(generate_timeline_html(years, st.session_state.current_year_index), unsafe_allow_html=True)

# JavaScript pour mettre à jour la ligne temporelle lorsque l'utilisateur fait défiler
st.markdown("""
<script>
    // Fonction pour mettre à jour l'affichage quand une nouvelle section est visible
    window.addEventListener('message', (e) => {
        if (e.data.type === 'streamlit:setComponentValue') {
            // Recharger la page avec le nouvel index (simuler une mise à jour)
            window.location.reload();
        }
    });
</script>
""", unsafe_allow_html=True)