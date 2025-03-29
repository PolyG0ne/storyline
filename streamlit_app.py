import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(layout="wide", page_title="Timeline 1980-2030")

# Titre de l'application
st.title("Ligne temporelle 1980-2030")

# Années à afficher (de 1980 à 2030 par intervalles de 2 ans)
years = list(range(1980, 2031, 2))

# Initialisation de l'état de session
if 'current_year_index' not in st.session_state:
    st.session_state.current_year_index = 0

# Style CSS amélioré - roulette plus haute avec plus d'années visibles
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
        padding: 30px 0;
        border-radius: 10px;
        z-index: 1000;
        width: 100px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
        height: 400px;  /* Augmentation de la hauteur */
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .year-slot {
        margin: 12px 0;
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
    
    .year-extreme {
        opacity: 0.1;
    }
    
    .main-content {
        margin-left: 120px;
    }
    
    /* Effet de fondu en haut et en bas */
    .timeline-fade-top, .timeline-fade-bottom {
        position: fixed;
        left: 2rem;
        width: 100px;
        height: 70px;
        z-index: 1001;
        pointer-events: none;
    }
    
    .timeline-fade-top {
        top: calc(50% - 200px);
        background: linear-gradient(to bottom, 
                    rgba(255,255,255,1) 0%, 
                    rgba(255,255,255,0) 100%);
    }
    
    .timeline-fade-bottom {
        top: calc(50% + 130px);
        background: linear-gradient(to top, 
                    rgba(255,255,255,1) 0%, 
                    rgba(255,255,255,0) 100%);
    }
    
    /* Style pour les ancres de section */
    .year-section-anchor {
        scroll-margin-top: 50vh;
    }
    
    /* Cacher les composants Streamlit qui gèrent la communication */
    #timeline-communication {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour générer le HTML de la ligne temporelle avec plus d'années visibles
def generate_timeline_html(years, current_index):
    timeline_html = '<div class="timeline-container">'
    
    # Afficher 9 années: 4 au-dessus, l'année courante, et 4 en-dessous
    visible_years = 9
    half_visible = visible_years // 2
    
    for i in range(max(0, current_index-half_visible), min(len(years), current_index+half_visible+1)):
        if i == current_index:
            class_name = "year-slot year-current"
        elif i == current_index-1 or i == current_index+1:
            class_name = "year-slot year-above" if i < current_index else "year-slot year-below"
        elif i == current_index-2 or i == current_index+2:
            class_name = "year-slot year-far"
        elif i == current_index-3 or i == current_index+3:
            class_name = "year-slot year-edge"
        else:
            class_name = "year-slot year-extreme"
        
        timeline_html += f'<div class="{class_name}" data-year-index="{i}">{years[i]}</div>'
    
    timeline_html += '</div>'
    
    # Ajouter les effets de fondu en haut et en bas
    timeline_html += '<div class="timeline-fade-top"></div>'
    timeline_html += '<div class="timeline-fade-bottom"></div>'
    
    return timeline_html

# Création de deux colonnes: une invisible pour l'espace et une pour le contenu principal
_, main_col = st.columns([1, 4])

# Élément caché pour la communication avec JavaScript
timeline_communication = st.empty()
timeline_communication.markdown('<div id="timeline-communication"></div>', unsafe_allow_html=True)

# Créer des sections pour chaque année
with main_col:
    st.header("Contenu principal")
    st.write("Faites défiler la page pour voir la ligne temporelle se déplacer comme une roue du temps.")
    
    # Créer un contenu suffisamment long pour permettre le défilement
    for i, year in enumerate(years):
        # Marquer la section avec un id pour la référence JS
        st.markdown(f'<div id="year-section-{i}" class="year-section-anchor"></div>', unsafe_allow_html=True)
        
        st.subheader(f"Section de l'année {year}")
        st.write(f"Contenu pour l'année {year}. Continuez à défiler pour voir l'effet de 'machine à sous' sur la ligne temporelle.")
        
        # Ajouter du contenu factice pour chaque année
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate eu pharetra nec, mattis ac neque.")
        st.write("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
        
        # Ajouter un séparateur et plus d'espace pour rendre le défilement plus fluide
        st.markdown("---")
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Afficher la ligne temporelle (fixe sur le côté gauche)
st.markdown(generate_timeline_html(years, st.session_state.current_year_index), unsafe_allow_html=True)

# JavaScript pour la détection de défilement et mise à jour de la ligne temporelle
# Cette fois, nous utilisons la méthode IntersectionObserver de manière plus efficace
js_code = """
<script>
    // Attendre que tous les éléments soient chargés
    document.addEventListener('DOMContentLoaded', function() {
        // Sélectionner tous les éléments de section d'année
        const yearSections = document.querySelectorAll('[id^="year-section-"]');
        
        // Créer l'observateur d'intersection
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Extraire l'index de l'année à partir de l'ID
                    const yearId = entry.target.id;
                    const yearIndex = parseInt(yearId.split('-').pop());
                    
                    // Mettre à jour la timeline sans recharger toute la page
                    updateTimeline(yearIndex);
                }
            });
        }, { 
            threshold: 0.5,  // Déclencher lorsque 50% de la section est visible
            rootMargin: "-10% 0px -10% 0px"  // Ajuster la zone de détection
        });
        
        // Observer chaque section
        yearSections.forEach(section => {
            observer.observe(section);
        });
        
        // Fonction pour mettre à jour la timeline sans recharger la page
        function updateTimeline(currentIndex) {
            // Mettre à jour les classes des éléments de la timeline
            const timelineItems = document.querySelectorAll('.timeline-container .year-slot');
            
            timelineItems.forEach(item => {
                const itemIndex = parseInt(item.getAttribute('data-year-index'));
                
                // Mettre à jour les classes en fonction de la position relative
                item.className = 'year-slot';
                
                if (itemIndex === currentIndex) {
                    item.classList.add('year-current');
                } else if (itemIndex === currentIndex - 1 || itemIndex === currentIndex + 1) {
                    item.classList.add(itemIndex < currentIndex ? 'year-above' : 'year-below');
                } else if (itemIndex === currentIndex - 2 || itemIndex === currentIndex + 2) {
                    item.classList.add('year-far');
                } else if (itemIndex === currentIndex - 3 || itemIndex === currentIndex + 3) {
                    item.classList.add('year-edge');
                } else {
                    item.classList.add('year-extreme');
                }
            });
            
            // Mettre à jour l'état de session côté serveur en utilisant Streamlit
            const streamlitMessageChannel = window.parent.streamlitMessageChannel;
            if (streamlitMessageChannel) {
                streamlitMessageChannel.notifyChannelToStreamlit('streamlit:setComponentValue', {
                    "id": "timeline-communication",
                    "value": currentIndex
                });
            }
        }
    });
</script>
"""

st.markdown(js_code, unsafe_allow_html=True)

# Composants complémentaires dans la barre latérale
with st.sidebar:
    st.title("Informations")
    st.metric("Année courante", years[st.session_state.current_year_index])
    
    # Navigation rapide avec select_slider
    selected_year = st.select_slider(
        "Naviguer rapidement",
        options=years,
        value=years[st.session_state.current_year_index]
    )
    
    # Si l'année sélectionnée change, mettre à jour l'index
    if selected_year != years[st.session_state.current_year_index]:
        new_index = years.index(selected_year)
        st.session_state.current_year_index = new_index
        # Forcer un rechargement pour mettre à jour la position de défilement
        st.rerun()
    
    # Option pour personnaliser l'affichage
    st.divider()
    st.subheader("Personnalisation")
    timeline_color = st.color_picker("Couleur de l'année actuelle", "#1E88E5")
    
    # Appliquer la personnalisation dynamiquement
    st.markdown(f"""
    <style>
        .year-current {{
            color: {timeline_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)