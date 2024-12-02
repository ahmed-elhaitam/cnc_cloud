import streamlit as st

# Page d'accueil
st.title("Système de Recommandation CNC")
st.write("Bienvenue sur notre plateforme de recommandation des formations d'ingénieurs pour les étudiants du CNC.")

# Authentification
auth_status = st.sidebar.selectbox("Connexion", ["Se connecter", "S'inscrire"])
if auth_status == "Se connecter":
    st.sidebar.text_input("Email")
    st.sidebar.text_input("Mot de passe", type="password")
    st.sidebar.button("Connexion")
elif auth_status == "S'inscrire":
    st.sidebar.text_input("Nom")
    st.sidebar.text_input("Email")
    st.sidebar.text_input("Mot de passe", type="password")
    st.sidebar.button("Inscription")

# Recommandation
st.subheader("Formations recommandées")
formations = [
    {"Nom": "Génie Informatique", "Etablissement": "EMI", "Débouchés": "Ingénieur logiciel, Data Scientist"},
    {"Nom": "Génie Civil", "Etablissement": "EHTP", "Débouchés": "Chef de projet, Consultant en BTP"}
]

for i, formation in enumerate(formations):
    st.write(f"**{formation['Nom']}** - {formation['Etablissement']}")
    st.write(f"Débouchés : {formation['Débouchés']}")
    if st.button(f"Voir plus {i}"):  # Bouton unique basé sur l'index
        st.write(f"Vous avez sélectionné : {formation['Nom']}")
