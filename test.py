import streamlit as st
import sqlite3
from datetime import datetime

# Connexion à la base de données
connection = sqlite3.connect("salle_de_sport.db")  # Remplacez par votre chemin
cursor = connection.cursor()

# Requête SQL pour extraire les données
query = """
SELECT capacite_max, id, coach_id, sport, horaire, nombre_inscrits
FROM cours;
"""
cursor.execute(query)
rows = cursor.fetchall()  # Récupérer les données sous forme de liste de tuples

# Optionnel : transformation des données
formatted_rows = []
for row in rows:
    capacite_max, id_, coach_id, sport, horaire, nombre_inscrits = row
    formatted_rows.append(
        {
            "Capacité Max": capacite_max,
            "ID": id_,
            "Coach ID": coach_id,
            "Sport": sport,
            "Nombre Inscrits": nombre_inscrits,
        }
    )

# Affichage des données dans Streamlit
st.title("Liste des Cours")
st.table(formatted_rows)  # Affiche les données sous forme de tableau
