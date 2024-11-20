import streamlit as st
import sqlite3
from sqlmodel import Field, Session, SQLModel, create_engine, select 
from sqlalchemy import select, engine

connection = sqlite3.connect("salle_de_sport.db") 
cursor = connection.cursor()



st.sidebar.title("Menu principal")
choix = st.sidebar.radio("Choisissez une rubrique :", ["Consulter les cours disponibles", "S'inscrire à un cours", "Annuler une inscription", "Consulter l'historique des inscriptions"])



class Base(Decl)


def display():
    if choix == "Consulter les cours disponibles":
        st.title("Cours disponibles")



        # def selectionner_donnees(cours):
        #     with Session(engine) as session :
        #         requete = select(cours)
        #         resultats = session.exec(requete)
        #         return resultats.all()
            
        #     selectionner_donnees(cours)
        

        with Session(engine) as session :
            cours = session.exec(cours).all()
            for e in cours : 
                print(f"{e.id}")


        

        




 
    
        




    elif choix == "S'inscrire à un cours":
        pass
    elif choix == "Annuler une inscription":
        pass
    elif choix == "Consulter l'historique des inscriptions":
        pass
   



display()







        # def selection():
        #     stmt = select *.where(table = )
        #     with Session

        # query = """
        # SELECT * FROM cours 
        # """

        # cursor.execute(query)
        # options = cursor.fetchall()

        # formatted_options = [
        #     f"{horaire} - {libelle} ({places_restantes} places restantes)" 
        #     for horaire, libelle, places_restantes in options
        #     ]


        # selection = st.multiselect(
        #     "Sélectionner un ou plusieurs créneaux disponibles :", 
        #     formatted_options
        # )

        # st.markdown(f"Les créneaux sélectionnés : {', '.join(selection) if selection else 'Aucun'}")