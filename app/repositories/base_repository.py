import datetime
from typing import Any, Dict, List, Optional, Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from ..database import db


class BaseRepository(object):
    model_class = db.Model
    has_uuid = False

    def __init__(self, database: Optional[SQLAlchemy]) -> None:
        self.db = database

    def all(self) -> List[db.Model]:
        return self.model_class.query.all()

    def get(self,
            offset: int,
            limit: int,
            order: Any = None) -> List[db.Model]:
        query = self.model_class.query
        if order is not None:
            query = query.order_by(order)

        return query.offset(offset).limit(limit).all()

    def create(self, fields: Dict) -> db.Model:
        model = self.model_class(**fields)
        self.db.session.add(model)
        if not self.db.session.info['in_transaction']:
            self.db.session.commit()
        return model

    def update(self, model: db.Model, fields: Dict) -> db.Model:
        for key in fields:
            setattr(model, key, fields[key])
        self.db.session.add(model)
        if not self.db.session.info['in_transaction']:
            self.db.session.commit()
        return model

    def delete(self, model: db.Model) -> bool:
        if getattr(model, '__soft_delete__', False):
            model.deleted_at = datetime.datetime.utcnow()
            self.db.session.add(model)
        else:
            self.db.session.delete(model)

        if not self.db.session.info['in_transaction']:
            self.db.session.commit()
        return True

    def find(self, primary_id: Any) -> db.Model:
        return self.model_class.query.filter_by(id=primary_id).first()

    def exist(self, primary_id: Union[int, str]) -> bool:
        return bool(self.model_class.query.filter_by(id=primary_id).first())

    def first_by_filter(self,
                        filter_dict: Dict = None,
                        offset: int = 0,
                        limit: int = 10,
                        order: str = "id",
                        direction: str = "asc") -> Optional[db.Model]:
        if filter_dict is None:
            filter_dict = {}

        query = self.build_order_query(self.model_class.query, order,
                                       direction)

        query = self.build_filter_query(query, filter_dict)

        return query.offset(offset).limit(limit).first()

    def get_by_filter(self,
                      filter_dict: Dict = None,
                      offset: int = 0,
                      limit: int = 10,
                      order: str = "id",
                      direction: str = "asc") -> List[db.Model]:
        if filter_dict is None:
            filter_dict = {}

        query = self.build_order_query(self.model_class.query, order,
                                       direction)

        query = self.build_filter_query(query, filter_dict)

        return query.offset(offset).limit(limit).all()

    def count_by_filter(self, filter_dict: Dict = None) -> int:
        if filter_dict is None:
            filter_dict = {}
        query = self.model_class.query

        query = self.build_filter_query(query, filter_dict)

        return query.count()

    def all_by_filter(self, filter_dict: Dict = None) -> List[db.Model]:
        if filter_dict is None:
            filter_dict = {}
        query = self.model_class.query

        query = self.build_filter_query(query, filter_dict)

        return query.all()

    def update_by_filter(self, filter_dict: Dict,
                         fields: Dict) -> Optional[List[db.Model]]:
        if not filter_dict:
            return None

        if not fields:
            return None

        fields_ = {}
        columns = self.model_class.__table__.columns.keys()
        for key in fields:
            if key in columns:
                fields_[key] = fields[key]

        if not fields_:
            return None

        query = self.model_class.query

        query = self.build_filter_query(query, filter_dict)

        updated = query.update(fields_, synchronize_session='fetch')

        if not self.db.session.info['in_transaction']:
            self.db.session.commit()

        return updated

    def delete_by_filter(self, filter_dict: Dict) -> Optional[List[db.Model]]:
        if not filter_dict:
            return None

        query = self.model_class.query

        query = self.build_filter_query(query, filter_dict)

        deleted = query.delete(synchronize_session='fetch')

        if not self.db.session.info['in_transaction']:
            self.db.session.commit()

        return deleted

    def build_filter_query(self, query, filter_dict: Dict = None):
        if filter_dict is None:
            filter_dict = {}

        return query.filter_by(**filter_dict)

    def build_order_query(self,
                          query,
                          order: str = "id",
                          direction: str = "asc"):
        columns = self.model_class.__table__.columns.keys()
        # if order not in columns, override order as id
        if order not in columns:
            order = 'id'

        # if direction not in [asc, desc], override direction
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        return query.order_by(
            text(self.model_class.__tablename__ + "." + order + " " +
                 direction))
