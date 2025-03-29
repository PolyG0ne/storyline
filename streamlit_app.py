import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from streamlit.runtime.state import SessionState

# Configuration de la page avec thèmes modernes
st.set_page_config(
    page_title="Mon Parcours Professionnel",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io/community',
        'About': "# Application de parcours professionnel\nCréée avec Streamlit"
    }
)

# Utilisation de st.cache_data pour optimiser le chargement des données
@st.cache_data(ttl=3600)
def load_experiences():
    """Charge les expériences depuis un stockage persistant"""
    if "experiences" not in st.session_state:
        # Si aucune donnée en session, essayer de charger depuis un fichier
        try:
            if os.path.exists("experiences.json"):
                with open("experiences.json", "r") as f:
                    st.session_state.experiences = json.load(f)
            else:
                # Données d'exemple par défaut
                st.session_state.experiences = [
                    {
                        "date": "2023 - Présent",
                        "titre": "Développeur Full Stack",
                        "description": "Développement d'applications web modernes utilisant Python, React et AWS.",
                        "image_path": None,
                        "competences": ["Python", "React", "AWS", "Docker", "CI/CD"]
                    },
                    {
                        "date": "2020 - 2023",
                        "titre": "Ingénieur Logiciel",
                        "description": "Conception et développement de solutions logicielles pour le secteur financier.",
                        "image_path": None,
                        "competences": ["Java", "Spring Boot", "PostgreSQL", "Microservices"]
                    },
                    {
                        "date": "2018 - 2020",
                        "titre": "Développeur Backend",
                        "description": "Création d'APIs RESTful et optimisation des performances de bases de données.",
                        "image_path": None,
                        "competences": ["Python", "Django", "MongoDB", "REST API"]
                    },
                    {
                        "date": "2016 - 2018",
                        "titre": "Développeur Junior",
                        "description": "Première expérience professionnelle dans le développement de sites web.",
                        "image_path": None,
                        "competences": ["HTML/CSS", "JavaScript", "PHP", "MySQL"]
                    }
                ]
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            st.session_state.experiences = []
    
    return st.session_state.experiences

def save_experiences():
    """Sauvegarde les expériences dans un stockage persistant"""
    try:
        with open("experiences.json", "w") as f:
            json.dump(st.session_state.experiences, f)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des données: {e}")
        return False

# Fonction pour créer un CSS personnalisé qui utilise les fonctionnalités natives de Streamlit
def load_custom_css():
    st.markdown("""
    <style>
        /* Style pour la timeline moderne */
        .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        .timeline-container {
            position: relative;
            padding-left: 30px;
            transition: all 0.3s ease;
        }
        
        .timeline-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 10px;
            width: 4px;
            height: 100%;
            background-color: var(--primary-color, #3498db);
            border-radius: 4px;
        }
        
        .timeline-point {
            position: absolute;
            left: 0;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background-color: var(--primary-color, #3498db);
            border: 4px solid white;
            margin-top: 15px;
            box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.2);
        }
        
        .experience-card {
            background-color: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            border-left: 4px solid var(--primary-color, #3498db);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .experience-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.12);
        }
        
        .date-badge {
            background-color: var(--primary-color, #3498db);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 12px;
        }
        
        /* Style pour les tags de compétences */
        .skill-tag {
            display: inline-block;
            background-color: rgba(52, 152, 219, 0.1);
            color: var(--primary-color, #3498db);
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 13px;
            margin-right: 8px;
            margin-bottom: 8px;
            border: 1px solid rgba(52, 152, 219, 0.2);
        }
        
        /* Support du thème sombre */
        @media (prefers-color-scheme: dark) {
            .experience-card {
                background-color: rgba(30, 30, 30, 0.6);
            }
            
            .skill-tag {
                background-color: rgba(52, 152, 219, 0.2);
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Fonction pour créer un élément de timeline avec animations natives de Streamlit
def create_timeline_item(date, titre, description, image_path=None, competences=None):
    # Utiliser des containers Streamlit pour l'animation
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        # Colonne de gauche pour la timeline
        with col1:
            st.markdown(f"""
            <div class="timeline-container">
                <div class="timeline-point"></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Colonne de droite pour le contenu
        with col2:
            # Utiliser st.container pour appliquer l'animation
            card_container = st.container()
            
            with card_container:
                st.markdown(f"""
                <div class="experience-card">
                    <div class="date-badge">{date}</div>
                    <h3>{titre}</h3>
                """, unsafe_allow_html=True)
                
                # Affichage de l'image si fournie
                if image_path:
                    st.image(image_path, use_column_width=True, caption=titre)
                
                st.markdown(f"<p>{description}</p>", unsafe_allow_html=True)
                
                # Affichage des compétences avec des tags modernes
                if competences and len(competences) > 0:
                    st.markdown("<h4>Compétences acquises</h4>", unsafe_allow_html=True)
                    # Utiliser des colonnes pour afficher les compétences en grille
                    skill_html = '<div style="display: flex; flex-wrap: wrap;">'
                    for comp in competences:
                        skill_html += f'<div class="skill-tag">{comp}</div>'
                    skill_html += '</div>'
                    st.markdown(skill_html, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Ajouter un espace entre les éléments
        st.markdown("<br>", unsafe_allow_html=True)

def main():
    # Charger le CSS personnalisé
    load_custom_css()
    
    # Afficher un titre moderne avec emoji
    st.title("✨ Mon Parcours Professionnel")
    st.write("Une chronologie interactive de mes expériences professionnelles.")
    st.divider()
    
    # Système d'onglets modernes
    tab1, tab2 = st.tabs(["📋 Parcours", "➕ Administration"])
    
    with tab1:
        # Charger les expériences
        experiences = load_experiences()
        
        # Créer la timeline avec animation
        if experiences:
            for exp in experiences:
                create_timeline_item(
                    exp["date"],
                    exp["titre"],
                    exp["description"],
                    exp.get("image_path"),
                    exp.get("competences", [])
                )
        else:
            st.info("Aucune expérience n'a été ajoutée. Utilisez l'onglet Administration pour ajouter votre parcours.")
    
    with tab2:
        st.header("Ajouter une nouvelle expérience")
        
        # Formulaire moderne avec validation
        with st.form("nouvelle_experience", clear_on_submit=True):
            date = st.text_input("Date (ex: 2023 - Présent)", 
                placeholder="Entrez la période de cette expérience")
            
            titre = st.text_input("Titre du poste", 
                placeholder="Ex: Développeur Full Stack")
            
            description = st.text_area("Description", 
                placeholder="Décrivez vos responsabilités et réalisations...")
            
            # Upload d'image moderne
            image_upload = st.file_uploader("Image (optionnel)", 
                type=["jpg", "jpeg", "png"],
                help="Ajoutez une image représentative de cette expérience")
            
            # Champ de compétences interactif
            competences_input = st.text_area("Compétences (une par ligne)", 
                placeholder="Python\nReact\nAWS")
            
            # Vérification basique des champs obligatoires avec message d'information
            if not date or not titre or not description:
                st.info("Les champs Date, Titre et Description sont obligatoires.")
            
            submit_button = st.form_submit_button("Ajouter à la timeline")
            
            if submit_button:
                # Validation des données
                if not date or not titre or not description:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                else:
                    # Traitement de l'image
                    image_path = None
                    if image_upload is not None:
                        # Créer un dossier pour les images si nécessaire
                        os.makedirs("images", exist_ok=True)
                        # Sauvegarder l'image
                        image_path = f"images/{datetime.now().strftime('%Y%m%d%H%M%S')}_{image_upload.name}"
                        with open(image_path, "wb") as f:
                            f.write(image_upload.getbuffer())
                    
                    # Traitement des compétences
                    competences_list = []
                    if competences_input:
                        competences_list = [comp.strip() for comp in competences_input.split("\n") if comp.strip()]
                    
                    # Créer l'objet expérience
                    nouvelle_experience = {
                        "date": date,
                        "titre": titre,
                        "description": description,
                        "image_path": image_path,
                        "competences": competences_list
                    }
                    
                    # Ajouter à la liste des expériences
                    if "experiences" not in st.session_state:
                        st.session_state.experiences = []
                    
                    st.session_state.experiences.append(nouvelle_experience)
                    
                    # Sauvegarder les données
                    if save_experiences():
                        # Notification moderne avec toast
                        st.toast("✅ Expérience ajoutée avec succès!")
                        # Forcer le rechargement des données
                        st.experimental_rerun()
                    else:
                        st.error("Erreur lors de la sauvegarde des données.")
        
        # Option pour supprimer ou modifier des expériences existantes
        if "experiences" in st.session_state and st.session_state.experiences:
            st.divider()
            st.subheader("Gérer les expériences existantes")
            
            for i, exp in enumerate(st.session_state.experiences):
                with st.expander(f"{exp['date']} - {exp['titre']}"):
                    st.write(f"**Description:** {exp['description']}")
                    
                    if st.button(f"Supprimer cette expérience", key=f"delete_{i}"):
                        # Supprimer l'expérience
                        del st.session_state.experiences[i]
                        # Sauvegarder les modifications
                        if save_experiences():
                            st.toast("🗑️ Expérience supprimée!")
                            st.experimental_rerun()

if __name__ == "__main__":
    main()