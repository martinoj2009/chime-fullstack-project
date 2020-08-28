from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref

from .Base import db


class tag(db.Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True)
    menu_item_id = db.relationship('menu_item', backref=backref('menu_item'), lazy=True)

    def __repr__(self):
        return {'id': self.id, 'name': self.name}
