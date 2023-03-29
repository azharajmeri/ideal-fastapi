import functools
import logging
import re
import time
from typing import Any

from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from sqlalchemy import create_engine, inspect, Engine, event
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from core.config import app_config
from core.exceptions import NotFoundError

engine = create_engine(
    app_config.DATABASE_URL
)

# Useful for identifying slow or n + 1 queries. But doesn't need to be enabled in production.
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.debug("Start Query: %s", statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)


SessionLocal = sessionmaker(bind=engine)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


raise_attribute_error = object()


def resolve_attr(obj, attr, default=None):
    """Attempts to access attr via dotted notation, returns none if attr does not exist."""
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def _id_str(self):
        if ids := inspect(self).identity:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    f"{self.__class__} has incorrect attribute '{key}' in __repr__attrs__"
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = f"{value[:max_length]}..."

            if wrap_in_quote:
                value = f"'{value}'"
            values.append(value if single else f"{key}:{value}")

        return " ".join(values)

    def __repr__(self):
        # get id like '#123'
        id_str = f"#{self._id_str}" if self._id_str else ""
        # join class name, id and repr_attrs
        return f'<{self.__class__.__name__} {id_str}{f" {self._repr_attrs_str}" if self._repr_attrs_str else ""}>'


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    return request.state.db


def get_model_name_by_tablename(table_fullname: str) -> str:
    """Returns the model name of a given table."""
    return get_class_by_tablename(table_fullname=table_fullname).__name__


def get_class_by_tablename(table_fullname: str) -> Any:
    """Return class reference mapped to table."""

    def _find_class(name):
        for c in Base._decl_class_registry.values():
            if hasattr(
                    c, "__table__") and c.__table__.fullname.lower() == name.lower():
                return c

    mapped_name = resolve_table_name(table_fullname)
    mapped_class = _find_class(mapped_name)

    # try looking in the 'dispatch_core' schema
    if not mapped_class:
        mapped_class = _find_class(f"dispatch_core.{mapped_name}")

    if not mapped_class:
        raise ValidationError(
            [
                ErrorWrapper(
                    NotFoundError(msg="Model not found. Check the name of your model."),
                    loc="filter",
                )
            ],
            model=BaseModel,
        )

    return mapped_class


def get_table_name_by_class_instance(class_instance: Base) -> str:
    """Returns the name of the table for a given class instance."""
    return class_instance._sa_instance_state.mapper.mapped_table.name
