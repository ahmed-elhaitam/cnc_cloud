import streamlit as st
import pandas as pd

def search_by_keyword(df, keyword):
    """
    Recherche de formations par mot-clé dans les colonnes binaires
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes binaires
        keyword (str): Mot-clé de recherche
    
    Returns:
        pd.DataFrame: Formations correspondantes
    """
    # Convertir le mot-clé en minuscules
    keyword = keyword.lower()
    
    # Rechercher dans les colonnes binaires
    binary_columns = [col for col in df.columns if col not in ['Institution', 'Formation', 'Débouchés', 'Preprocessed Debouches']]
    
    # Colonnes où le mot-clé est présent
    matching_columns = [col for col in binary_columns if keyword in col.lower()]
    
    # Filtrer les lignes où ces colonnes sont à 1
    if matching_columns:
        results = df[df[matching_columns].eq(1).any(axis=1)]
        return results[['Institution', 'Formation', 'Débouchés']]
    else:
        return pd.DataFrame(columns=['Institution', 'Formation', 'Débouchés'])

def main():
    # Titre de l'application
    st.title("🔍 Recherche de Formations par Mot-Clé")
    
    # Charger les données
    @st.cache_data
    def load_data():
        # Charger directement depuis le chemin du fichier
        return pd.read_csv('formation.csv')  # Remplacez par le chemin réel
    
    # Gérer les erreurs de chargement
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")
        return
    
    # Informations sur le dataset
    st.sidebar.header("Informations du Dataset")
    st.sidebar.write(f"Nombre total de formations : {len(df)}")
    st.sidebar.write(f"Colonnes disponibles : {', '.join(df.columns)}")
    
    # Champ de saisie pour le mot-clé
    st.sidebar.header("Recherche de Formations")
    keyword = st.sidebar.text_input("Entrez un mot-clé")
    
    # Bouton de recherche
    if st.sidebar.button("Rechercher"):
        if keyword:
            # Rechercher les formations
            results = search_by_keyword(df, keyword)
            
            # Afficher les résultats
            if not results.empty:
                st.success(f"✅ {len(results)} formation(s) trouvée(s)")
                st.dataframe(results)
            else:
                st.warning("❌ Aucune formation trouvée pour ce mot-clé")
        else:
            st.warning("Veuillez saisir un mot-clé")
    
    # Section informative
    st.sidebar.info("""
    ### Comment utiliser l'application
    - Saisissez un mot-clé dans le champ de recherche
    - La recherche se fait sur les colonnes binaires prétraitées
    - Les résultats sont affichés en temps réel
    """)

# Exécuter l'application
if __name__ == "__main__":
    main()
