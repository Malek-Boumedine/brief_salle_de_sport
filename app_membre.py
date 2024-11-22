import streamlit as st
import sqlite3
from sqlmodel import Field, Session, SQLModel, create_engine, select 
from sqlalchemy import select, engine
from utils import *

connection = sqlite3.connect("salle_de_sport.db") 
cursor = connection.cursor()

st.sidebar.title("Menu principal")
choix = st.sidebar.radio("Choisissez une rubrique :", ["Consulter les cours disponibles", "Consulter l'historique des inscriptions", "S'inscrire à un cours", "Annuler une inscription"])

def display():
    if choix == "Consulter les cours disponibles":

        query = """
        SELECT capacite_max, id, coach_id, sport, horaire, nombre_inscrits
        FROM cours;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        st.title("Cours disponibles")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.write("🆔 \n ##### ID")
        col2.write("👩‍🏫 \n ##### Coach ID")
        col3.write("🏅 \n ##### Sport")
        col4.write("⏰ \n ##### Horaires")
        col5.write("👥 \n ##### Nombre d'inscrits")
        col6.write ("🏋️ \n  ##### Capacité Max")

        for row in rows:
            capacite_max, id_, coach_id, sport, horaire, nombre_inscrits = row
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write(id_) 
            col2.write(coach_id)
            col3.write(sport)
            col4.write(horaire)
            col5.write(nombre_inscrits)
            col6.write(capacite_max)

    elif choix == "S'inscrire à un cours" : 

        # requete liste des cours
        query = """
        SELECT capacite_max, id, coach_id, sport, horaire, nombre_inscrits
        FROM cours;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # requete liste des membres
        query_membres = """
        SELECT id, nom, prenom
        FROM Membre;
        """
        cursor.execute(query_membres)
        rows2 = cursor.fetchall()
        membre_a_ajouter = st.selectbox("choisissez un membre", rows2)
        id_membre = membre_a_ajouter[0]

        # affichage colonne et titre
        st.title("S'inscrire à un cours")

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        col1.write("🆔 \n ##### ID")
        col2.write("👩‍🏫 \n ##### Coach ID")
        col3.write("🏅 \n ##### Sport")
        col4.write("⏰ \n ##### Horaires")
        col5.write("👥 \n ##### Nombre d'inscrits")
        col6.write ("🏋️ \n  ##### Capacité Max")
        col7.write("🎯 \n ##### Choisir un cours")

        for row in rows:
            capacite_max, id_, coach_id, sport, horaire, nombre_inscrits = row
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            col1.write(capacite_max)
            col2.write(id_)
            col3.write(coach_id)
            col4.write(sport)
            col5.write(horaire)
            col6.write(nombre_inscrits)
            
            # bouton choisir
            if col7.button("Choisir", key=f"button_{id_}"):
                query_inscription = """
                INSERT INTO Inscription (id_membre, id_cours, date_inscription)
                VALUES (?, ?, ?)
                """
                cursor.execute(query_inscription, (id_membre, id_, datetime.now().date()))
                connection.commit()
                
                # Maj nb inscrits pour le cours
                query_nb_inscrit = """
                UPDATE Cours 
                SET nombre_inscrits = nombre_inscrits + 1
                WHERE id = ?
                """
                cursor.execute(query_nb_inscrit, (id_,))
                connection.commit()
                
                st.success(f"Cours {id_} sélectionné !")
                st.rerun()  

    elif choix == "Consulter l'historique des inscriptions":

        st.title("Consulter l'historique des inscriptions")

        id_saisi = st.number_input("Saisissez votre identifiant", min_value=1, step=1)

        if id_saisi:
            # Utilisation de l'identifiant dans la requête pour filtrer les résultats
            query = """
            SELECT id_cours 
            FROM inscription
            WHERE id_membre = ?
            """
            
            # Exécution de la requête avec l'identifiant saisi
            cursor.execute(query, (id_saisi,))  # Passer l'id_saisi comme paramètre

            rows = cursor.fetchall()

            if rows:
                st.write("Voici les cours où vous êtes inscrit :")
                for row in rows:
                    st.write(f"- Cours ID : {row[0]}")
            else:
                st.write("Aucun cours trouvé pour cet identifiant.")

    elif choix == "Annuler une inscription":

        st.title("Annuler une inscription")

        id_saisi = st.number_input("Saisissez votre identifiant", min_value=1, step=1)
        
        if id_saisi:
            # Utilisation de l'identifiant dans la requête pour filtrer les résultats
            query = """
            SELECT id_cours 
            FROM inscription
            WHERE id_membre = ?
            """
            
            # Exécution de la requête avec l'identifiant saisi
            cursor.execute(query, (id_saisi,))  # Passer l'id_saisi comme paramètre

            rows = cursor.fetchall()

            if rows:
                st.write("Voici les cours où vous êtes inscrit :")
                for row in rows:
                    st.write(f"- Cours ID : {row[0]}")
            else:
                st.write("Aucun cours trouvé pour cet identifiant.")

        cours_saisi = st.number_input("Saisissez le cours à annuler :", min_value=1, step=1)

        # JUSQUE LA OK
            
        # query = "SELECT id_cours FROM inscription WHERE id_membre = ?"
        # cursor.execute(query, (id_saisi,))
        # result = cursor.fetchall()

        # if cours_saisi in cursor.execute(query, (id_saisi,)) :
            
        query_annulation = """
        DELETE
        FROM inscription
        WHERE id_membre = ? 
        """

            
        if st.button("Se désinscrire du cours"):
            #execution de la requete
            cursor.execute(query_annulation, (cours_saisi,))  # id_saisi comme paramètre
            # st.success(f"Cours {id_} sélectionné !")
            connection.commit()

            query_nb_inscrit = """
            UPDATE Cours 
            SET nombre_inscrits = nombre_inscrits - 1
            WHERE id = ? 
        
            """
            cursor.execute(query_nb_inscrit, (cours_saisi,))
            connection.commit() 
            st.rerun() 

        #     ////
        

        # if cours_saisi in [row[0] for row in result]:  # Assurez-vous que cours_saisi est au bon format
        #     query_annulation = """
        #     DELETE
        #     FROM inscription
        #     WHERE id_membre = ? AND id = ?
        #     """
            
        #     if st.button("Se désinscrire du cours"):
        #         # Désinscription
        #         cursor.execute(query_annulation, (id_saisi, cours_saisi))
        #         st.write("Vous avez bien été désinscrit du cours")
        #         connection.commit()

display()


