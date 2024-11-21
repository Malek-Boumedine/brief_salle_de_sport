import sqlmodel import Session, select 


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, Session

class Base(DeclarativeBase):
    pass

class Cours(Base):
    __tablename__ = "salle_de_sport"
    id = Column(Integer, primary_key=True)
    id_sport = Column(Integer)  
    horaire = Column(String)
    capacite_max
    nombre_inscrits =
    coach_id = 
    

engine = create_engine("sqlite:///salle_de_sport.db")
Base.metadata.create_all(engine)

with Session(engine) as session :
    fct1 = session.query(Cours).all()



    # for e in cours:
    #     print(f"{e.id} - {e.nom}")  # Assure-toi que ces attributs existent


    id: int | None = Field(default=None, primary_key=True)
    id_sport : int | None = Field(default=None, foreign_key="sport.id", ondelete="CASCADE")
    horaire : datetime | None = Field(nullable=False)
    capacite_max : int | None = Field(nullable=False)
    nombre_inscrits : int | None = Field(nullable=False)
    coach_id : int | None = Field(default=None, foreign_key="coach.id", ondelete="CASCADE")