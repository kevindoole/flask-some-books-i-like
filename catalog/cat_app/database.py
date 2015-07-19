from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cat_app

print cat_app.app.config['DATABASE']

engine = create_engine(cat_app.app.config['DATABASE'], convert_unicode=True)
session_factory = sessionmaker(autoflush=False, bind=engine)
db_session = scoped_session(session_factory)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db_tables():
    import models
    Base.metadata.create_all(bind=engine)
