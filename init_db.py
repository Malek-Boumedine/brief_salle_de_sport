from models import *
from sqlmodel import SQLModel, create_engine


sqlite_file_name = "salle_de_sport.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def init_db() :
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__" : 
    init_db()
