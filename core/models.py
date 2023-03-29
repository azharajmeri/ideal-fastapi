from datetime import datetime

from sqlalchemy import Column, DateTime


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
