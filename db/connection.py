from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from settings import Settings

try:
    engine = create_engine(Settings().DATABASE_URL)
    session_maker = sessionmaker(autoflush=False, autocommit=False, bind=engine)

except OperationalError as err:
    pass
