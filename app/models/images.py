from .. import db
from .motorcycles import Motorcycle


motorcycle_img_association = db.Table(
    'motorcycle_img_association',
    db.Column('motorcycle_id', db.Integer, db.ForeignKey('motorcycle.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('motorcycleimage.id'), primary_key=True)
)

class MotorcycleImage(db.Model):
    __tablename__ = 'motorcycleimage'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    image = db.relationship(
        "Motorcycle", secondary=motorcycle_img_association
    )

