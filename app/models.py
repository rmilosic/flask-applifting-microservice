from datetime import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from . import db


class Offer(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    price = db.Column(db.String(120), unique=True, nullable=False)
    items_in_stock = db.Column(db.String(120), nullable=False)
    found_date = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'),
        nullable=False)
    
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