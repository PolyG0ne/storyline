import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Mon Parcours Professionnel",
    page_icon="🧠",
    layout="wide"
)

# Ajout de CSS personnalisé pour la timeline
st.markdown("""
<style>
    /* Style pour la timeline */
    .timeline-container {
        position: relative;
        padding-left: 30px;
    }
    
    /* Ligne verticale */
    .timeline-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 10px;
        width: 4px;
        height: 100%;
        background-color: #3498db;
        border-radius: 4px;
    }
    
    /* Point de la timeline */
    .timeline-point {
        position: absolute;
        left: 0;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #3498db;
        border: 4px solid white;
        margin-top: 15px;
    }
    
    /* Animation au défilement */
    .timeline-item {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    
    .timeline-item.visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Style pour les cartes d'expérience */
    .experience-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    
    /* Ajustements pour les images */
    .experience-image {
        border-radius: 8px;
        max-width: 100%;
        margin-bottom: 15px;
    }
    
    /* Pour les dates */
    .date-badge {
        background-color: #3498db;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>

<script>
    // Script JavaScript pour l'animation au défilement
    document.addEventListener('DOMContentLoaded', function() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {threshold: 0.1});
        
        document.querySelectorAll('.timeline-item').forEach(item => {
            observer.observe(item);
        });
    });
</script>
""", unsafe_allow_html=True)

# Titre de l'application
st.title("Mon Parcours Professionnel")
st.markdown("---")

# Fonction pour créer un élément de timeline
def create_timeline_item(date, titre, description, image=None, compétences=None):
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
        st.markdown(f"""
        <div class="timeline-item">
            <div class="experience-card">
                <div class="date-badge">{date}</div>
                <h3>{titre}</h3>
        """, unsafe_allow_html=True)
        
        # Affichage de l'image si fournie
        if image:
            st.image(image, use_column_width=True, caption=titre, output_format="JPEG")
        
        st.markdown(f"<p>{description}</p>", unsafe_allow_html=True)
        
        # Affichage des compétences si fournies
        if compétences:
            st.markdown("<h4>Compétences acquises :</h4>", unsafe_allow_html=True)
            for comp in compétences:
                st.markdown(f"- {comp}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Espacement entre les éléments
    st.markdown("<br>", unsafe_allow_html=True)

# Exemple de données pour la timeline - À remplacer par vos propres expériences
expériences = [
    {
        "date": "2023 - Présent",
        "titre": "Développeur Full Stack",
        "description": "Développement d'applications web modernes utilisant Python, React et AWS.",
        "image": "https://via.placeholder.com/600x300",  # Remplacer par le chemin vers votre image
        "compétences": ["Python", "React", "AWS", "Docker", "CI/CD"]
    },
    {
        "date": "2020 - 2023",
        "titre": "Ingénieur Logiciel",
        "description": "Conception et développement de solutions logicielles pour le secteur financier.",
        "image": "https://via.placeholder.com/600x300",  # Remplacer par le chemin vers votre image
        "compétences": ["Java", "Spring Boot", "PostgreSQL", "Microservices"]
    },
    {
        "date": "2018 - 2020",
        "titre": "Développeur Backend",
        "description": "Création d'APIs RESTful et optimisation des performances de bases de données.",
        "image": "https://via.placeholder.com/600x300",  # Remplacer par le chemin vers votre image
        "compétences": ["Python", "Django", "MongoDB", "REST API"]
    },
    {
        "date": "2016 - 2018",
        "titre": "Développeur Junior",
        "description": "Première expérience professionnelle dans le développement de sites web.",
        "image": "https://via.placeholder.com/600x300",  # Remplacer par le chemin vers votre image
        "compétences": ["HTML/CSS", "JavaScript", "PHP", "MySQL"]
    }
]

# Créer la timeline
for exp in expériences:
    create_timeline_item(
        exp["date"],
        exp["titre"],
        exp["description"],
        exp.get("image"),
        exp.get("compétences")
    )

# Section pour ajouter une nouvelle expérience (pour l'administrateur)
st.markdown("---")
st.header("Ajouter une nouvelle expérience")

with st.expander("Ouvrir le formulaire"):
    with st.form("nouvelle_experience"):
        date = st.text_input("Date (ex: 2023 - Présent)")
        titre = st.text_input("Titre du poste")
        description = st.text_area("Description")
        image_upload = st.file_uploader("Image (optionnel)", type=["jpg", "jpeg", "png"])
        competences = st.text_area("Compétences (une par ligne)")
        
        submit_button = st.form_submit_button("Ajouter à la timeline")
        
        if submit_button:
            # Logique pour sauvegarder les données (à implémenter selon vos besoins)
            # Par exemple, vous pourriez les sauvegarder dans un fichier CSV ou une base de données
            st.success("Expérience ajoutée avec succès!")
            
            # Pour cet exemple, nous affichons simplement les données
            st.write("Données ajoutées :")
            st.write({
                "date": date,
                "titre": titre,
                "description": description,
                "image": "Chargée" if image_upload is not None else "Aucune",
                "compétences": competences.split("\n") if competences else []
            })

# Fonction pour sauvegarder les expériences dans un fichier CSV
def save_experiences_to_csv(experiences, filename="experiences.csv"):
    # Convertir en dataframe
    df = pd.DataFrame(experiences)
    # Sauvegarder en CSV
    df.to_csv(filename, index=False)
    return True

# Fonction pour charger les expériences depuis un fichier CSV
def load_experiences_from_csv(filename="experiences.csv"):
    try:
        df = pd.read_csv(filename)
        # Convertir en liste de dictionnaires
        experiences = df.to_dict('records')
        return experiences
    except:
        return []

# Ces fonctions peuvent être utilisées pour persister les données de votre parcours
# et les charger automatiquement au démarrage de l'application