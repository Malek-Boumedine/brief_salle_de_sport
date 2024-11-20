import streamlit as st
import sqlite3
from sqlmodel import Field, Session, SQLModel, create_engine, select 
from sqlalchemy import select, engine
from utils import *

connection = sqlite3.connect("salle_de_sport.db") 
cursor = connection.cursor()



st.sidebar.title("Menu principal")
choix = st.sidebar.radio("Choisissez une rubrique :", ["Consulter les cours disponibles", "S'inscrire à un cours", "Annuler une inscription", "Consulter l'historique des inscriptions"])




def display():
    if choix == "Consulter les cours disponibles":
        st.title("Cours disponibles")

        selectionner_donnees(Cours)

    
    elif choix == "S'inscrire à un cours":
        st.title("S'inscire à un cours")

        inserer_donnees(Cours)
















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