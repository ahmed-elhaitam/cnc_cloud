import streamlit as st

# Page d'accueil
st.title("Système de Recommandation CNC")
st.write("Bienvenue sur notre plateforme de recommandation des formations d'ingénieurs pour les étudiants du CNC.")

# Étape 1 : Saisie des informations de l'étudiant
st.sidebar.header("Profil Étudiant")
nom = st.sidebar.text_input("Nom")
email = st.sidebar.text_input("Email")
classement = st.sidebar.number_input("Classement CNC", min_value=1, max_value=5000, step=1)
filiere = st.sidebar.selectbox("Filière choisie", ["MP", "PSI", "TSI"])
interets = st.sidebar.text_area("Mots-clés d'intérêt (ex: IA, Génie Civil, Énergie)")

if st.sidebar.button("Enregistrer le profil"):
    st.sidebar.success("Profil enregistré avec succès !")

# Étape 2 : Recommandation des formations
st.subheader("Formations recommandées")

formations = [
    {"Nom": "Génie Informatique", "Etablissement": "EMI", 
     "Débouchés": "Ingénieur logiciel, Data Scientist", "Mots-clés": "Informatique, IA, Programmation"},
    {"Nom": "Génie Civil", "Etablissement": "EHTP", 
     "Débouchés": "Chef de projet, Consultant en BTP", "Mots-clés": "Construction, BTP, Environnement"},
    {"Nom": "Ingénierie des Données", "Etablissement": "ENSIAS", 
     "Débouchés": "Data Analyst, Ingénieur Big Data", "Mots-clés": "Data Science, IA, Cloud"}
]

# Filtrer les formations selon les intérêts de l'étudiant
if interets:
    mots_cles = [mot.strip().lower() for mot in interets.split(",")]
    formations = [
        formation for formation in formations
        if any(mot in formation["Mots-clés"].lower() for mot in mots_cles)
    ]

if not formations:
    st.write("Aucune formation ne correspond à vos mots-clés. Essayez d'élargir vos intérêts.")
else:
    for i, formation in enumerate(formations):
        st.write(f"**{formation['Nom']}** - {formation['Etablissement']}")
        st.write(f"Débouchés : {formation['Débouchés']}")
        st.write(f"Mots-clés : {formation['Mots-clés']}")
        if st.button(f"Voir plus {i}"):  # Bouton unique basé sur l'index
            st.write(f"Vous avez sélectionné : {formation['Nom']}")

# Étape 3 : Paiement des frais de dossier
st.subheader("Paiement des frais de dossier")

# Simuler un paiement
frais_paye = False
if st.checkbox("J'accepte de payer les frais de dossier (500 MAD / 50€)"):
    if st.button("Payer maintenant"):
        frais_paye = True
        st.success("Paiement effectué avec succès !")
        st.balloons()

if frais_paye:
    st.write("Votre paiement a été enregistré. Vous recevrez une confirmation par email.")

# Note : Vous pouvez intégrer un système de paiement réel comme Stripe ou PayPal ici
