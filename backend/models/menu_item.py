from sqlalchemy import Column, Integer, String, ForeignKey, Float
from flask import jsonify
from .Base import db


# Example model for your data structure
class menu_item(db.Model):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    description = Column(String(1000))
    tag = Column(Integer, ForeignKey('tags.id'))
    price = Column(Float, default=0)

    def __repr__(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price}
