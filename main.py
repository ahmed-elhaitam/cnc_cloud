import streamlit as st

# Titre de l'application
st.title("Application d'inscription des utilisateurs")

# Formulaire pour collecter les informations de l'utilisateur
with st.form("user_form"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    gmail = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    submitted = st.form_submit_button("Soumettre")

    if submitted:
        # Vérifier que tous les champs sont remplis
        if nom and prenom and gmail and password:
            try:
                # Connexion à la base de données
                connection = connect_to_database()
                # Insérer les données
                insert_user(connection, nom, prenom, gmail, password)
                st.success("Utilisateur ajouté avec succès !")
            except Exception as e:
                st.error(f"Erreur : {e}")
            finally:
                if 'connection' in locals():
                    connection.close()
        else:
            st.error("Tous les champs doivent être remplis.")

# Afficher les utilisateurs existants
st.subheader("Liste des utilisateurs existants")
try:
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT nom, prenom, gmail FROM utilisateurs")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    # Afficher les résultats dans un tableau
    if rows:
        st.table(rows)
    else:
        st.write("Aucun utilisateur trouvé.")
except Exception as e:
    st.error(f"Erreur lors de la récupération des utilisateurs : {e}")
