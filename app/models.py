from datetime import datetime
import uuid
import json

from sqlalchemy.dialects.postgresql import UUID

from . import db

class Offer(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    seller_id = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.String(120), nullable=False)
    found_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'),
        nullable=False)
    
    @property
    def serialize(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "price": self.price,
            "items_in_stock": self.items_in_stock,
            "found_date": self.found_date,
            "product_id": self.product_id
        }

    def __repr__(self):
        return '<Offer %r>' % self.id

class Product(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=True, default=None)
    deleted = db.Column(db.DateTime, nullable=True, default=None) 
    offers = db.relationship('Offer', backref='product', lazy=True)
    
    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created": self.created,
            "updated": self.updated,
            "deleted": self.deleted
        }
    
    def __repr__(self):
        return '<Product %r>' % self.name