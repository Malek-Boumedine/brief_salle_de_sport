from faker import Faker
import random

fake = Faker('fr_FR')  
liste_sports = ["Boxe", "Pilates", "Crossfit", "Grit", "TRX", "HIIT", "Bodybuilding", "Yoga"]
nombre_cours = 10
nombre_membres = 100
nombre_coachs = 10

########################################################################

def creer_personne():
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
    # id_carteAcces = 

    return {
        "prenom": prenom,
        "nom": nom,
        "genre": genre,
        "date_naissance": date_naissance,
        "email": email,
        "telephone": telephone,
    }

########################################################################

def creer_carte_acces ():
    numero_unique = fake.unique.random_int(min=10000, max=99999)
    return {
    "numero_unique": numero_unique,
  }

########################################################################

def creer_coach():
    genre = random.choice(["Masculin", "Feminin"])
    if genre == "Masculin":
        prenom = fake.first_name_male()
        nom = fake.last_name_male()
    else:
        prenom = fake.first_name_female()
        nom = fake.last_name_female()
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=65)
    email = f"{prenom.lower()}.{nom.lower()}@{fake.free_email_domain()}"
    telephone = fake.phone_number()
    id_sport = random.randint(1, len(liste_sports))
    
    return {
        "prenom": prenom,
        "nom": nom,
        "genre": genre,
        "date_naissance": date_naissance,
        "email": email,
        "telephone": telephone,
        "id_sport": id_sport,
    }

########################################################################

def creer_tous_les_sports():
    sports = []
    for sport in liste_sports:
        sports.append({
            "libelle": sport
        })
    return sports

########################################################################

def creer_cours():
    id_sport = random.randint(1, len(liste_sports))
    horaire = fake.date_time_this_year()
    capacite_max = random.randint(20, 30)  # Capacité maximale entre 20 et 30
    nombre_inscrits = random.randint(0, capacite_max)  # Nombre d'inscrits ne peut pas dépasser la capacité

    return {
        "id_sport": id_sport,
        "horaire": horaire.strftime("%Y-%m-%d %H:%M:%S"),
        "capacite_max": capacite_max,
        "nombre_inscrits": nombre_inscrits,
    }

########################################################################

def creer_inscription():
    id_membre = random.randint(1, nombre_membres)
    id_cours = random.randint(1, nombre_cours)
    date_inscription = fake.date_this_year()

    return {
        "id_membre": id_membre,
        "id_cours": id_cours,
        "date_inscription": date_inscription,
    }

########################################################################


if __name__ == "__main__" : 
    
    
    for _ in range(3):
        print(creer_personne())
    print(("="*20))

    for i in range(3) :
        print(creer_carte_acces())
    print(("="*20))
    
    for i in range(3) :
        print(creer_coach())
    print(("="*20))
        
    print(creer_tous_les_sports())
    print(("="*20))
    
    for i in range(3) :
        print(creer_cours())
    print(("="*20))
    
    for i in range(3) :
        creer_inscription()
    print(("="*20))
        
    

