from .. import db


class Sale(db.Model):
    __tablename__ = 'sale'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    salesperson_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    motorcycle_id = db.Column(db.ForeignKey('motorcycle.id'), nullable=False)
