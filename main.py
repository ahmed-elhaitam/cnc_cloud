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

# Fonction pour appeler l'API avec toutes les données
def call_azure_api():
    input_data = {
        "Inputs": {
            "input1": [
                {
                    "Institution": "AIAC",
                    "Formation": "Génie Informatique",
                    "Debouches": "Software Developer, Data Engineer"
                },
                {
                    "Institution": "EHTP",
                    "Formation": "Big Data",
                    "Debouches": "Data Analyst, Data Scientist"
                },
                {
                    "Institution": "EMI",
                    "Formation": "Génie Électrique",
                    "Debouches": "Electrical Engineer, Cloud Architect"
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

# Fonction pour filtrer les résultats contenant un mot-clé
def filter_results(data, keyword):
    df = pd.DataFrame(data)
    filtered_df = df[df["Debouches"].str.contains(keyword, case=False, na=False)]
    return filtered_df

# Interface utilisateur Streamlit
st.title("Recherche de Formations par Mot-clé")
st.markdown("Entrez un mot-clé pour trouver les formations pertinentes.")

# Entrée utilisateur
user_input = st.text_input("Entrez un mot-clé (exemple : data)")

if st.button("Rechercher"):
    if user_input:
        st.write(f"**Mot-clé saisi :** {user_input}")
        with st.spinner("Recherche en cours..."):
            # Appeler l'API pour obtenir toutes les formations
            results = call_azure_api()
            if "error" not in results:
                # Récupérer les résultats bruts
                data = results.get("Results", {}).get("output1", [])
                if data:
                    # Filtrer les résultats pour le mot-clé
                    filtered_df = filter_results(data, user_input)
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
