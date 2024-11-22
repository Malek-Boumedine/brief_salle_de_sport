from sqlmodel import Field, SQLModel, create_engine, Relationship, Session, select
from pydantic import EmailStr, ValidationError, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import date, datetime
from typing import List, Optional


sqlite_file_name = "salle_de_sport.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)



class Membre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prenom : str | None = Field(default=None, nullable=False)
    nom : str | None = Field(default=None, nullable=False)
    # genre : bool | None = Field(default=None, nullable=False)
    genre: str | None = Field(default=None, nullable=False)
    date_naissance : date | None = Field(default=None, nullable=False)
    email : EmailStr | None = Field(default=None, nullable=False, unique=True)
    telephone : PhoneNumber | None = Field(default=None, nullable=False, unique=True)
    id_carteAcces : int | None = Field(default=None, foreign_key="carteacces.id", ondelete="CASCADE", unique=True)
    inscriptions: List["Inscription"] = Relationship(back_populates="membre")

    def __str__ () : 
        return "membre"
    
    @field_validator("genre")
    @classmethod
    def valider_genre(cls, valeur) : 
        if valeur is None or valeur.lower() not in ["masculin", "feminin"] : 
            raise ValueError("Le genre doit être être 'Masculin' ou 'Feminin'")
        return valeur

    @field_validator("prenom", "nom", "genre", "date_naissance", "email", "telephone")
    @classmethod
    def non_vide(cls, valeur, field) : 
        if valeur is None or not valeur:
            raise ValueError(f"Le champ {field.name} ne peut pas être vide")
        return valeur
    

##########################################################################################
    
class CarteAcces(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    numero_unique : int | None = Field(default=None, nullable=False, unique=True)
    # membre : Membre = Relationship(back_populates="membre")
    
    @field_validator("numero_unique")
    @classmethod
    def non_vide(cls, valeur) : 
        if valeur is None or not valeur : 
            raise ValueError("le 'numero_unique' ne doit pas être vide")
        return valeur
    
    def __str__ () : 
        return "carte d'accès"



##########################################################################################

class Coach(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    prenom : str | None = Field(nullable=False)
    nom : str | None = Field(nullable=False)
    sport : str | None
    genre: str | None = Field(default=None, nullable=False)
    date_naissance : date | None = Field(default=None, nullable=False)
    email : str | None = Field(default=None, nullable=False, unique=True)
    telephone : str | None = Field(default=None, nullable=False, unique=True)
    
    def __str__ () : 
        return "coach"



##########################################################################################

class Cours(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sport : str | None
    horaire : datetime | None = Field(nullable=False, unique=True)
    capacite_max : int | None = Field(nullable=False)
    nombre_inscrits : int | None = Field(nullable=False)
    coach_id : int | None = Field(default=None, foreign_key="coach.id")
    inscriptions: List["Inscription"] = Relationship(back_populates="cours")
    
    def __str__ () : 
        return "cours"


    @field_validator("horaire")
    def cours_unique(cls, valeur) : 
        with Session(engine) as session :
            horaires = session.exec(select(Cours.horaire).all())
            if valeur in horaires : 
                raise ValueError("Cet horaire est déja pris")
        return valeur

##########################################################################################

class Inscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_membre : int | None = Field(default=None, foreign_key="membre.id", ondelete="CASCADE")
    id_cours : int| None = Field(default=None, foreign_key="cours.id", ondelete="CASCADE")
    date_inscription : date | None = Field(nullable=False)
    membre: Membre = Relationship(back_populates="inscriptions")
    cours: Cours = Relationship(back_populates="inscriptions")
    
    def __str__ () : 
        return "inscription"


##########################################################################################


if __name__ == "__main__" : 

    sqlite_file_name = "salle_de_sport.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)