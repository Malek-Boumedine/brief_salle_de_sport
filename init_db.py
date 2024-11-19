from models import *
from sqlmodel import SQLModel, create_engine


def init_db():
    sqlite_file_name = "salle_de_sport.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)


init_db()