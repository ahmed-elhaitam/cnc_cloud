import streamlit as st
import requests

# URL et clé API
ENDPOINT_URL = "http://efaf59fc-4db7-4538-8e15-427a1132bcfa.francecentral.azurecontainer.io/score"
API_KEY = "XD5TD2k91k03Fbr1jK6jskmTrXM4OzLN"

# Configuration des en-têtes
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Fonction pour appeler l'API Azure
def call_azure_api(data):
    try:
        response = requests.post(ENDPOINT_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Interface utilisateur Streamlit
st.title("Recommandation de Formations")
st.markdown("Entrez un mot-clé ou une description pour recevoir des recommandations.")

# Entrée utilisateur
user_input = st.text_input("Entrez un mot-clé ou une description (exemple : Data Scientist)")

# Bouton pour soumettre la requête
if st.button("Rechercher"):
    if user_input:
        # Préparer les données pour l'API
        input_data = {
            "Inputs": {
                "WebServiceInput": [{"Keyword": user_input}]
            }
        }

        st.write("**Requête envoyée à l'API :**")
        st.json(input_data)

        # Appeler l'API et afficher les résultats
        with st.spinner("Chargement..."):
            results = call_azure_api(input_data)
            if "error" not in results:
                st.success("Voici les résultats :")
                st.json(results)
            else:
                st.error(f"Erreur API : {results['error']}")
    else:
        st.warning("Veuillez entrer un mot-clé.")
