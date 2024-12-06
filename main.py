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
    binary_columns = [col for col in df.columns if col not in ['Institution', 'Formation', 'Debouches', 'Preprocessed Debouches']]
    
    # Colonnes où le mot-clé est présent
    matching_columns = [col for col in binary_columns if keyword in col.lower()]
    
    # Filtrer les lignes où ces colonnes sont à 1
    if matching_columns:
        results = df[df[matching_columns].eq(1).any(axis=1)]
        return results[['Institution', 'Formation']]
    else:
        return pd.DataFrame(columns=['Institution', 'Formation'])

def main():
    # Titre de l'application
    st.title("🔍 Recherche de Formations par Mot-Clé")
    
    # Charger les données
    @st.cache_data
    def load_data():
        return pd.read_csv('formation.csv')  # Remplacez par le chemin réel du fichier
    
    # Charger les données
    try:
        df = load_data()
        st.write("Colonnes disponibles dans le DataFrame :", df.columns.tolist())
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")
        return
    
    # Champ de saisie pour le mot-clé
    keyword = st.text_input("Entrez un mot-clé (exemple : data, cloud, AI, etc.)")
    
    # Bouton de recherche
    if st.button("Rechercher"):
        if keyword:
            results = search_by_keyword(df, keyword)
            if not results.empty:
                st.success(f"✅ {len(results)} formation(s) trouvée(s) pour le mot-clé '{keyword}'")
                st.dataframe(results)
            else:
                st.warning(f"❌ Aucune formation trouvée pour le mot-clé '{keyword}'")
        else:
            st.warning("Veuillez saisir un mot-clé")

# Exécuter l'application
if __name__ == "__main__":
    main()
