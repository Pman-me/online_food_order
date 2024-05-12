from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db_session


class BaseRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session
