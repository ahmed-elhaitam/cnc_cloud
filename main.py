import streamlit as st
import requests
import pandas as pd

# Configuration de l'endpoint Azure
ENDPOINT_URL = "http://efaf59fc-4db7-4538-8e15-427a1132bcfa.francecentral.azurecontainer.io/score"
API_KEY = "XD5TD2k91k03Fbr1jK6jskmTrXM4OzLN"  # Remplacez par votre clé API

# En-têtes pour l'API
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Fonction pour appeler l'API avec une requête correcte
def call_azure_api(keyword):
    input_data = {
        "Inputs": {
            "input1": [
                {
                    "Institution": "Dummy Institution",
                    "Formation": "Dummy Formation",
                    "Debouches": keyword
                }
            ]
        },
        "GlobalParameters": {}
    }
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=input_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

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
                # Convertir les résultats en DataFrame pour affichage
                data = results.get("Results", {}).get("output1", [])
                if data:
                    df = pd.DataFrame(data)
                    st.success("Voici les formations pertinentes :")
                    st.dataframe(df)
                else:
                    st.warning("Aucune donnée disponible.")
            else:
                st.error(f"Erreur API : {results['error']}")
    else:
        st.warning("Veuillez entrer un mot-clé.")
