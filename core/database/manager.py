import uuid
from typing import Any, Dict

from sqlalchemy.orm import Session

from core.database.core import Base
from core.utils import to_dict

DataObject = Dict[str, Any]


class QueryManager:

    @classmethod
    def get_single_item_by_filters(cls, fields: list, session: Session) -> Any:
        item: Base = session.query(cls).filter(*fields)
        item: Any = item.first()
        return item

    @classmethod
    def create_with_uuid(cls, data: DataObject, session: Session) -> DataObject:
        data.update({"id": str(uuid.uuid4())})
        item: Base = cls(**data)
        session.add(item)
        return item
