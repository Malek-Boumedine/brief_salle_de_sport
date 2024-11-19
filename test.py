from sqlmodel import Field, Session, SQLModel, create_engine
from models import *



def create_db_and_tables():

    sqlite_file_name = "salle_de_sport.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)


create_db_and_tables()    