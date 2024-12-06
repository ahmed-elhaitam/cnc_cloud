import streamlit as st
import requests
import pandas as pd

# URL et clé API
ENDPOINT_URL = "http://efaf59fc-4db7-4538-8e15-427a1132bcfa.francecentral.azurecontainer.io/score"
API_KEY = "XD5TD2k91k03Fbr1jK6jskmTrXM4OzLN"  # Remplacez par votre clé API

# En-têtes pour l'API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Fonction pour appeler l'API Azure
def call_azure_api(keyword):
    input_data = {
        "Inputs": {
            "input1": [{"Keyword": keyword}]
        },
        "GlobalParameters": {}
    }
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=input_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Fonction pour filtrer les formations ayant le mot-clé
def filter_results(data):
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(data)
    return df

# Interface utilisateur Streamlit
st.title("Recherche de Formations par Mot-clé")
st.markdown("Entrez un mot-clé pour trouver les formations pertinentes.")

# Entrée utilisateur
user_input = st.text_input("Entrez un mot-clé (exemple : data, cloud, AI, etc.)")

if st.button("Rechercher"):
    if user_input:
        st.write(f"**Mot-clé saisi :** {user_input}")
        with st.spinner("Recherche en cours..."):
            # Appeler l'API Azure
            results = call_azure_api(user_input)
            if "error" not in results:
                # Récupérer les résultats retournés par l'API
                data = results.get("Results", {}).get("output1", [])
                if data:
                    # Filtrer et afficher les formations
                    filtered_df = filter_results(data)
                    if not filtered_df.empty:
                        st.success("Formations pertinentes trouvées :")
                        st.dataframe(filtered_df)
                    else:
                        st.warning("Aucune formation ne correspond à ce mot-clé.")
                else:
                    st.warning("Aucun résultat disponible.")
            else:
                st.error(f"Erreur API : {results['error']}")
    else:
        st.warning("Veuillez entrer un mot-clé.")
