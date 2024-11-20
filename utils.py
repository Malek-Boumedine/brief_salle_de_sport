from sqlmodel import Session, select
from init_db import engine, init_db
# from populate_db import creer_liste_personnes
from models import *



init_db()


def selectionner_donnees(nom_table):
    with Session(engine) as session:
        requete = select(nom_table)
        resultats = session.exec(requete)
        return resultats.all()


def select_where(nom_table, condition) :    # where(Hero.name == "Deadpond")    -> table.nom_colonne == "valeur"
    with Session(engine) as session:
        requete = select(nom_table).where(condition)
        resultats = session.exec(requete)
        return resultats.all()


def inserer_donnees(donnee) : 
    with Session(engine) as session:
        membre = Membre(**donnee)
        session.add(membre)
        session.commit()


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




selectionner_donnees(Cours)



# if __name__ == "__main__" : 
#     num_people_to_create = 25
#     # fake_people = creer_liste_personnes(num_people_to_create)
#     for person in fake_people:
#         inserer_donnees(person)

    



