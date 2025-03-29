import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Titre de l'application
st.title("Application avec règle temporelle (1980-2030)")

# Création de la mise en page avec colonnes
col1, col2 = st.columns([1, 3])

# Création de la règle temporelle dans la colonne de gauche
with col1:
    st.markdown("## Règle temporelle")
    
    # Création de la liste des années
    years = list(range(1980, 2031))
    
    # Création d'un DataFrame pour faciliter l'affichage
    df_years = pd.DataFrame({"Année": years})
    
    # Ajout d'un sélecteur pour choisir l'année active
    selected_year = st.select_slider(
        "Sélectionnez une année",
        options=years,
        value=2000
    )
    
    # Affichage de la règle temporelle
    for year in years:
        # Personnalisation de l'affichage en fonction de l'année sélectionnée
        if year == selected_year:
            st.markdown(f"### **{year}** ←")
        else:
            # Ajout d'espace entre les années pour permettre le défilement
            st.markdown(f"### {year}")
            st.markdown("<br>", unsafe=False)

# Contenu principal dans la colonne de droite
with col2:
    st.markdown(f"## Contenu pour l'année {selected_year}")
    st.write(f"Vous avez sélectionné l'année {selected_year}.")
    st.write("Ajoutez ici le contenu principal de votre application.")
    
    # Exemple de contenu qui change en fonction de l'année sélectionnée
    if selected_year < 1990:
        st.write("Période: Années 80")
    elif selected_year < 2000:
        st.write("Période: Années 90")
    elif selected_year < 2010:
        st.write("Période: Années 2000")
    elif selected_year < 2020:
        st.write("Période: Années 2010")
    else:
        st.write("Période: Années 2020")
    
    # Vous pouvez ajouter plus de contenu ici qui change en fonction de l'année sélectionnée