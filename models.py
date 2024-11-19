from sqlmodel import Field, SQLModel, create_engine
from sqlalchemy import UniqueConstraint, Column, String
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import date, datetime



class Membre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nom : str | None = Field(default=None, nullable=False)
    prenom : str | None = Field(default=None, nullable=False)
    date_naissance : date | None = Field(default=None, nullable=False)
    email : EmailStr | None = Field(default=None, nullable=False, unique=True)
    telephone : PhoneNumber | None = Field(default=None, nullable=False, unique=True)
    genre : bool | None = Field(default=None, nullable=False)
    id_carteAcces : int | None = Field(default=None, foreign_key="carteacces.id", ondelete="CASCADE", unique=True)

    
class CarteAcces(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    numero_unique : int | None = Field(default=None, nullable=False, unique=True)


class Coach(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_sport : int | None = Field(default=None, foreign_key="sport.id")
    nom : str | None = Field(nullable=False)
    prenom : str | None = Field(nullable=False)
    date_naissance : date | None = Field(default=None, nullable=False)
    email : str | None = Field(default=None, nullable=False, unique=True)
    telephone : str | None = Field(default=None, nullable=False, unique=True)
    
    
class Sport(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    libelle : str | None = Field(default=None, nullable=False)


class Cours(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_sport : int | None = Field(default=None, foreign_key="sport.id", ondelete="CASCADE")
    horaire : datetime | None = Field(nullable=False)
    capacite_max : int | None = Field(nullable=False)
    nombre_inscrits : int | None = Field(nullable=False)
    coach_id : int | None = Field(default=None, foreign_key="coach.id", ondelete="CASCADE")


class Inscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_membre : int | None = Field(default=None, foreign_key="membre.id", ondelete="CASCADE")
    id_cours : int| None = Field(default=None, foreign_key="cours.id", ondelete="CASCADE")
    date_inscription : date | None = Field(nullable=False)



if __name__ == "__main__" : 

    sqlite_file_name = "salle_de_sport.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)