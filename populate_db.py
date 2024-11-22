from faker import Faker
import random
from datetime import datetime
from models import Coach

fake = Faker('fr_FR')  


########################################################################

def creer_personne(liste_cartes : list):
    genre = random.choice(["Masculin", "Feminin"])
    if genre == "Masculin":
        prenom = fake.first_name_male()
        nom = fake.last_name_male()
    else:
        prenom = fake.first_name_female()
        nom = fake.last_name_female()
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=80)
    email = f"{prenom.lower()}.{nom.lower()}@{fake.free_email_domain()}"
    telephone = fake.phone_number()
    id_carteAcces = random.choice(liste_cartes)
    liste_cartes.remove(id_carteAcces)

    return {
        "prenom": prenom,
        "nom": nom,
        "genre": genre,
        "date_naissance": date_naissance,
        "email": email,
        "telephone": telephone,
        "id_carteAcces" : id_carteAcces
    }


########################################################################

def creer_carte_acces (): 
    numero_unique = fake.unique.random_int(min=10000, max=99999)
    
    return {
    "numero_unique": numero_unique,
    }

def liste_cartes_uniques(nombre_cartes : int) -> tuple[list[dict | int]] : 
    liste_nums = []
    for _ in range(nombre_cartes) :
        numero_unique = fake.unique.random_int(min=10000, max=99999)
        liste_nums.append(numero_unique)
    nums_uniques = list(set(liste_nums))
    liste_cartes = [{"numero_unique" : num} for num in nums_uniques]
    
    return nums_uniques, liste_cartes
    

########################################################################

def creer_coach(liste_sports):
    genre = random.choice(["Masculin", "Feminin"])
    if genre == "Masculin":
        prenom = fake.first_name_male()
        nom = fake.last_name_male()
    else:
        prenom = fake.first_name_female()
        nom = fake.last_name_female()
    sport = random.choice(liste_sports)
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=65)
    email = f"{prenom.lower()}.{nom.lower()}@{fake.free_email_domain()}"
    telephone = fake.phone_number()
    
    return {
        "prenom": prenom,
        "nom": nom,
        "sport" : sport,
        "genre": genre,
        "date_naissance": date_naissance,
        "email": email,
        "telephone": telephone,
    }


########################################################################

def creer_cours(liste_coachs : list["Coach"]):

    annee = 2024
    mois = random.randint(1,12)
    if mois in [1,3,5,7,8,10,12] : 
        jour = random.randint(1,31)
    elif mois in [4,6,9,11] : 
        jour = random.randint(1,30)
    else :
        jour = random.randint(1,28)
    heure = random.randint(9,17)
        
    horaire = datetime(annee, mois, jour, heure, 00, 00)
    capacite_max = random.randint(20, 30)  # Capacité maximale entre 20 et 30
    nombre_inscrits = random.randint(0, capacite_max)  # Nombre d'inscrits ne peut pas dépasser la capacité
    coach = random.choice(liste_coachs)
    coach_id = coach.id
    sport = coach.sport

    return {
        "sport": sport,
        "horaire" : horaire,
        "capacite_max": capacite_max,
        "nombre_inscrits": nombre_inscrits,
        "coach_id" : coach_id
    }

# date
# heure au lieu de horaire

########################################################################

def creer_inscription(nombre_cours, nombre_membres):
    id_membre = random.randint(1, nombre_membres)
    id_cours = random.randint(1, nombre_cours)
    date_inscription = fake.date_this_year()

    return {
        "id_membre": id_membre,
        "id_cours": id_cours,
        "date_inscription": date_inscription,
    }

########################################################################



