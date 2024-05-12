from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime

from db.base import SQLBASE


class BaseModel(SQLBASE):
    __abstract__ = True

    creator = Column(String(50))
    modifier = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    modified_at = Column(DateTime(timezone=True))
