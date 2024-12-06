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
    
    # Filtrer les lignes où le mot-clé a une colonne binaire à 1
    results = df[df[binary_columns].eq(1).any(axis=1)]
    results = results[results[binary_columns].columns[results[binary_columns].eq(1).any()].str.contains(keyword, case=False)]
    
    return results[['Institution', 'Formation', 'Débouchés']]

def main():
    # Titre de l'application
    st.title("🔍 Recherche de Formations par Mot-Clé")
    
    # Charger les données (intégrées dans le code)
    @st.cache_data
    def load_data():
        # Remplacez ceci par votre méthode de chargement de données
        data = pd.read_csv('formation.csv')  # À remplacer
        return data
    
    df = load_data()
    
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
