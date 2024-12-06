import streamlit as st
import pandas as pd

# Charger le dataset
df = pd.read_csv('formation.csv')  # Remplacez par le chemin de votre fichier

def recherche_formations(mot_cle):
    """
    Recherche des formations par mot-clé
    """
    # Convertir le mot-clé en minuscules
    mot_cle = mot_cle.lower()
    
    # Filtrer les formations 
    resultats = df[
        (df['Formation'].str.lower().str.contains(mot_cle)) | 
        (df['Débouchés'].str.lower().str.contains(mot_cle))
    ]
    
    return resultats

def main():
    st.title("🔍 Recherche de Formations par Mot-Clé")
    
    # Champ de saisie pour le mot-clé
    mot_cle = st.text_input("Entrez un mot-clé pour rechercher une formation")
    
    # Bouton de recherche
    if st.button("Rechercher"):
        if mot_cle:
            # Effectuer la recherche
            resultats = recherche_formations(mot_cle)
            
            # Afficher les résultats
            if not resultats.empty:
                st.success(f"{len(resultats)} formation(s) trouvée(s)")
                st.dataframe(resultats)
            else:
                st.warning("Aucune formation trouvée pour ce mot-clé")
        else:
            st.error("Veuillez saisir un mot-clé")

if __name__ == "__main__":
    main()
