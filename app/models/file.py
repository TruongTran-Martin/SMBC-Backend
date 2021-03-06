from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects import sqlite

from ..database import db


class File(db.Model):
    __tablename__ = 'files'

    class STORAGE:
        S3 = 's3'
        LOCAL = 'local'
        ADDITIONAL = 'additional'

    class MEDIA:
        VIDEO = 'video'

    id = db.Column('id',
                   db.BigInteger().with_variant(sqlite.INTEGER(), 'sqlite'),
                   primary_key=True)
    original_file_name = db.Column('original_file_name',
                                   db.String(255),
                                   nullable=True)
    url = db.Column('url', db.String(255), nullable=False)
    media_type = db.Column('media_type', db.String(255), nullable=True)
    storage_type = db.Column('storage_type', db.String(255), nullable=True)

    created_at = db.Column('created_at',
                           db.TIMESTAMP,
                           default=datetime.utcnow,
                           server_default=func.current_timestamp(),
                           nullable=False)
    updated_at = db.Column('updated_at',
                           db.TIMESTAMP,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow,
                           server_default=func.current_timestamp(),
                           nullable=False)

    def __repr__(self):
        return "<{name} '{id}'>".format(name=self.__class__.__name__,
                                        id=self.id)
