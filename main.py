import streamlit as st
import pandas as pd

def main():
    # Titre de l'application
    st.title("🔍 Recherche de Formations")
    
    # Téléchargement du fichier
    uploaded_file = st.file_uploader("Téléchargez votre fichier CSV", type=['csv'])
    
    if uploaded_file is not None:
        # Charger les données
        df = pd.read_csv(uploaded_file)
        
        # Barre latérale pour la recherche
        st.sidebar.header("Rechercher une Formation")
        
        # Options de recherche
        search_option = st.sidebar.selectbox(
            "Rechercher dans :",
            ["Formation", "Débouchés", "Institution"]
        )
        
        # Champ de saisie pour le mot-clé
        keyword = st.sidebar.text_input("Entrez un mot-clé")
        
        # Bouton de recherche
        if st.sidebar.button("Rechercher"):
            # Filtrer les données
            if keyword:
                results = df[df[search_option].str.contains(keyword, case=False, na=False)]
                
                # Afficher les résultats
                if not results.empty:
                    st.success(f"✅ {len(results)} formation(s) trouvée(s)")
                    st.dataframe(results)
                else:
                    st.warning("❌ Aucune formation trouvée")
            else:
                st.warning("Veuillez saisir un mot-clé")
        
        # Aperçu des données
        st.subheader("Aperçu des Données")
        st.dataframe(df)

# Exécuter l'application
if __name__ == "__main__":
    main()
