from .. import db


class Motorcycle(db.Model):
    __tablename__ = 'motorcycle'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255), nullable=False)
    manufactore_year = db.Column(db.Integer, nullable=False, index=True)
    model_year = db.Column(db.Integer, nullable=False, index=True)
    color = db.Column(db.String(15), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
