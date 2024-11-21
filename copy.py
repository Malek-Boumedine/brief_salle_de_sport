import sqlmodel
from sqlmodel import session, create_engine
engine = create_engine
SQLmodel.metadat.create_all(engine)

with session(engine) as session :
    cours1 = Cours(nom, horaire...)
    