from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from .. import db
from uuid import uuid4

class User(UserMixin, db.Model):
    _id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    _created = db.Column(db.DateTime(timezone=False))
    _deleted = db.Column(db.DateTime(timezone=False))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)

    def get_id(self):
        return self._id

