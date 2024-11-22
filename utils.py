from sqlmodel import Session, select
from init_db import engine, init_db
from populate_db import *
from models import *



init_db()


def selectionner_donnees(nom_classe):  
    with Session(engine) as session:  
        requete = select(nom_classe)
        resultats = session.exec(requete).all()
        return resultats


def inserer_donnees(donnee, nom_classe) -> None : 
    with Session(engine) as session:
        membre = nom_classe(**donnee)
        session.add(membre)
        session.commit()


def select_where(nom_classe, identifiant) :
    with Session(engine) as session:
        requete = select(nom_classe).where(getattr(nom_classe, id) == identifiant)
        resultats = session.exec(requete)
        return resultats.all()

        
def modifier_donnee(nom_classe, identifiant, colonne_a_modifier, nouvelle_valeur):
    with Session(engine) as session:
        statement = select(nom_classe).where(getattr(nom_classe, "id") == identifiant)
        resultats = session.exec(statement)
        r1 = resultats.one_or_none()

        if r1:
            setattr(r1, colonne_a_modifier, nouvelle_valeur)
            session.add(r1)
            session.commit()
            session.refresh(r1)
            return True
        return False


def supprimer_donnee(nom_classe, identifiant):
    with Session(engine) as session:
        statement = select(nom_classe).where(getattr(nom_classe, 'id') == identifiant)
        resultats = session.exec(statement)
        r1 = resultats.one_or_none()
        if r1:
            session.delete(r1)
            session.commit()



############################################################################################################








############################################################################################################

selectionner_donnees(Cours)

if __name__ == "__main__" : 
    
    liste_sports = ["Boxe", "Pilates", "Crossfit", "Grit", "TRX", "HIIT", "Bodybuilding", "Yoga"]

    # ################################
    nombre_cartes_acces = 2000
    liste_nums_cartes, liste_carte_acces = liste_cartes_uniques(nombre_cartes_acces)
    for carte in liste_carte_acces :
        inserer_donnees(carte, CarteAcces)


    # ################################
    nombre_membres = 1000
    for _ in range(nombre_membres) : 
        membre = creer_personne(liste_nums_cartes)
        inserer_donnees(membre, Membre)
        
    
    # ################################
    nombre_coachs = 100
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
    
