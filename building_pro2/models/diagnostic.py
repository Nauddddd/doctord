from .. import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

class Diagnosis(db.Model):
    _id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    _created = db.Column(db.DateTime(timezone=False))
    _deleted = db.Column(db.DateTime(timezone=False))
    _creator = db.Column(UUID(as_uuid=True), db.ForeignKey('user._id'))
    path = db.Column(db.String)

    def get_id(self):
        return self._id