from sqlmodel import Session, select
from init_db import engine, init_db
from populate_db import *
from models import *



init_db()


def selectionner_donnees(model_class):  
    with Session(engine) as session:  
        requete = select(model_class)
        resultats = session.exec(requete).all()
        return resultats


def inserer_donnees(donnee, nom_classe) -> None : 
    with Session(engine) as session:
        membre = nom_classe(**donnee)
        session.add(membre)
        session.commit()


def select_where(nom_table, condition) :    # where(Hero.name == "Deadpond")    -> table.nom_colonne == "valeur"
    with Session(engine) as session:
        requete = select(nom_table).where(condition)
        resultats = session.exec(requete)
        return resultats.all()


def update(table, condition, colonne_a_modifier, nouvelle_valeur) : 
    with Session(engine) as session:
        statement = select(table).where(condition)
        resultats = session.exec(statement)
        r1 = resultats.one()

        getattr(r1, colonne_a_modifier) == nouvelle_valeur
        session.add(r1)

        session.commit()
        session.refresh(r1)


def delete(table, condition) : 
    with Session(engine) as session:
        statement = select(table).where(condition)
        resultats = session.exec(statement)
        r1 = resultats.one()
        if r1 : 
            session.delete(r1)
            session.commit()
            print("Succès")
        else:
            print("La valeur n'existe pas")


############################################################################################################


if __name__ == "__main__" : 
    
    liste_sports = ["Boxe", "Pilates", "Crossfit", "Grit", "TRX", "HIIT", "Bodybuilding", "Yoga"]

    # ################################
    nombre_cartes_acces = 500
    liste_nums_cartes, liste_carte_acces = liste_cartes_uniques(nombre_cartes_acces)
    for carte in liste_carte_acces :
        inserer_donnees(carte, CarteAcces)


    # ################################
    nombre_membres = 100
    for _ in range(nombre_membres) : 
        membre = creer_personne(liste_nums_cartes)
        inserer_donnees(membre, Membre)
        
    
    # ################################
    nombre_coachs = 10
    for _ in range(nombre_coachs) : 
        coach = creer_coach(liste_sports)
        inserer_donnees(coach, Coach)
    
    liste_coachs = selectionner_donnees(Coach)
    # print(liste_coachs[0])
    
    
    # ################################
    nombre_cours = 20
    for _ in range(nombre_coachs) : 
        cours = creer_cours(liste_coachs)
        inserer_donnees(cours, Cours)


    # ################################
    nombre_inscriptions = 15
    for _ in range(nombre_cours, nombre_membres) : 
        inscription = creer_inscription(nombre_cours, nombre_membres)
        inserer_donnees(inscription, Inscription)
        
        
