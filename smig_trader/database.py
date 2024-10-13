from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common import settings

# Create the engine
engine = create_engine(settings.database_uri)

# Create a sessionmaker factory that will generate new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a session object to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
