import streamlit as st
import pandas as pd
import requests

# URL et clé API
ENDPOINT_URL = "http://efaf59fc-4db7-4538-8e15-427a1132bcfa.francecentral.azurecontainer.io/score"
API_KEY = "XD5TD2k91k03Fbr1jK6jskmTrXM4OzLN"  # Remplacez par votre clé API

# En-têtes de l'API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Fonction pour appeler l'API Azure
def call_azure_api(keyword):
    input_data = {
        "Inputs": {
            "WebServiceInput": [
                {"Keyword": keyword}
            ]
        }
    }
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=input_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Fonction pour filtrer les données
def filter_results(data, keyword):
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(data)
    if keyword in df.columns:
        # Filtrer les lignes où la colonne associée au mot-clé contient `1`
        filtered_df = df[df[keyword] == 1]
        return filtered_df
    else:
        return pd.DataFrame()  # Retourner un DataFrame vide si la colonne n'existe pas

# Interface utilisateur Streamlit
st.title("Recommandation de Formations")
st.markdown("Entrez un mot-clé pour voir les formations pertinentes.")

# Entrée utilisateur
user_input = st.text_input("Entrez un mot-clé (par exemple : data)")

if st.button("Rechercher"):
    if user_input:
        st.write(f"**Mot-clé saisi :** {user_input}")
        with st.spinner("Recherche en cours..."):
            # Appeler l'API
            results = call_azure_api(user_input)
            if "error" not in results:
                # Traiter les résultats
                data = results.get("Outputs", {}).get("WebServiceOutput", [])
                if data:
                    # Filtrer les résultats
                    filtered_df = filter_results(data, user_input)
                    if not filtered_df.empty:
                        st.success("Voici les formations pertinentes :")
                        st.dataframe(filtered_df)
                    else:
                        st.warning("Aucune formation trouvée pour ce mot-clé.")
                else:
                    st.warning("Résultats non disponibles ou format inattendu.")
            else:
                st.error(f"Erreur API : {results['error']}")
    else:
        st.warning("Veuillez entrer un mot-clé.")
