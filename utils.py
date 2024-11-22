from sqlmodel import Session, select
from init_db import engine, init_db
from populate_db import *
from models import *
from datetime import datetime, timedelta, time


def erreur1() : 
    return ValueError("Ce créneau est déja pris !")

def erreur2() : 
    return ValueError("Veuilez choisir un créneau de 9h à 16h (le dernier cours commence à 16h et se termine à 17h) !")    

init_db()


def selectionner_donnees(nom_classe):  
    with Session(engine) as session:  
        requete = select(nom_classe)
        resultats = session.exec(requete).all()
        return resultats

def afficher_cours():
    with Session(engine) as session:  
        requete = select(Cours.id, Cours.sport, Cours.horaire, Cours.capacite_max, Cours.nombre_inscrits, Cours.coach_id, (Coach.prenom + " " + Coach.nom).label("coach")).where(Cours.coach_id == Coach.id)
        resultats = session.exec(requete).all()
        return resultats

def afficher_membres() :
    with Session(engine) as session:
        membres = session.exec(select(Membre.id, Membre.prenom, Membre.nom)).all()
        return membres

def afficher_coachs() : 
    with Session(engine) as session:  
        requete = select(Coach.id, (Coach.prenom + " " + Coach.nom).label("coach"))
        resultats = session.exec(requete).all()
        return [{"id": r[0], "nom": r[1]} for r in resultats]
    
def afficher_inscriptions() :
    with Session(engine) as session:
        requete = select(Inscription.id,Inscription.id_membre, (Membre.nom + " " + Membre.prenom).label("membre"), Inscription.id_cours, Cours.sport.label("cours"), Inscription.date_inscription).where(Inscription.id_membre == Membre.id).where(Inscription.id_cours == Cours.id)
        resultats = session.exec(requete).all()
        return resultats

def inserer_donnees(donnees : dict, nom_classe : type[SQLModel]) -> None:
    with Session(engine) as session:
        if nom_classe == Membre:
            numero_unique = random.randint(10000, 99999)
            while session.exec(select(CarteAcces).where(CarteAcces.numero_unique == numero_unique)).first():
                numero_unique = random.randint(10000, 99999)
            carte = CarteAcces(numero_unique=numero_unique)
            session.add(carte)
            session.commit()
            session.refresh(carte)
            # Ajouter l'ID de la carte aux données du membre
            donnees["id_carteAcces"] = carte.id
        if nom_classe != Cours : 
        # Créer l'instance de la classe avec les données
            instance = nom_classe(**donnees)
            session.add(instance)
            session.commit()
            
        elif nom_classe == Cours : 
            horaires = session.exec(select(Cours.horaire)).all()
            if donnees["horaire"] in horaires : 
                return erreur1()

            # Vérification de l'heure
            heure_cours = donnees["horaire"].time()  # Extrait l'heure du datetime
            heure_min = time(9, 0)
            heure_max = time(16, 0)

            if heure_cours < heure_min or heure_cours > heure_max:
                return erreur2()

            # Si pas d'erreur, créer l'instance
            instance = nom_classe(**donnees)
            session.add(instance)
            session.commit()    
            heure_cours = donnees["horaire"].time()
            heure_min = time(9, 0)
            heure_max = time(16, 0)
            
            if heure_cours < heure_min or heure_cours > heure_max:
                return erreur2()
    return None
            

def modifier_donnee(nom_classe, identifiant, colonne_a_modifier, nouvelle_valeur):
    with Session(engine) as session:
        statement = select(nom_classe).where(getattr(nom_classe, "id") == identifiant)
        resultats = session.exec(statement)
        r1 = resultats.one_or_none()
        if r1:
            # Vérification spéciale pour les cours et l'horaire
            if nom_classe == Cours and colonne_a_modifier == "horaire":
                # Sélectionner tous les horaires sauf celui du cours actuel
                horaires = session.exec(select(Cours.horaire).where(Cours.id != identifiant)).all()
                # Vérifier si le nouvel horaire existe déjà
                if nouvelle_valeur in horaires:
                    return erreur1()
                # Vérifier si l'horaire est dans les plages autorisées
                heure = nouvelle_valeur.time()
                if heure < time(9, 0) or heure > time(16, 0):
                    return erreur2()
            # Si pas d'erreur, procéder à la modification
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

selectionner_donnees(Cours)

if __name__ == "__main__" : 
    
    liste_sports = ["Boxe", "Pilates", "Crossfit", "Grit", "TRX", "HIIT", "Bodybuilding", "Yoga"]

    # ################################
    nombre_membres = 10
    for _ in range(nombre_membres) : 
        membre = creer_personne()
        inserer_donnees(membre, Membre)
    
    # ################################
    nombre_coachs = 10
    for _ in range(nombre_coachs) : 
        coach = creer_coach(liste_sports)
        inserer_donnees(coach, Coach)
    
    liste_coachs = selectionner_donnees(Coach)
    
    
    # ################################
    nombre_cours = 20
    for _ in range(nombre_coachs) : 
        cours = creer_cours(liste_coachs)
        inserer_donnees(cours, Cours)


    # ################################
    nombre_inscriptions = 20
    for _ in range(nombre_inscriptions) : 
        inscription = creer_inscription(nombre_cours, nombre_membres)
        inserer_donnees(inscription, Inscription)

