import secrets
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask_mail import Message
from .. import db, mail


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    cpf = db.Column(db.String(11), nullable=True)
    rg = db.Column(db.String(9), nullable=True)
    birthdate = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    auth_token = db.Column(db.String(255))
    auth_token_expire = db.Column(db.DateTime)

    def generate_token(self):
        token = secrets.token_urlsafe(50)
        self.auth_token = token
        self.auth_token_expire = datetime.now() + relativedelta(minutes=30)
        db.session.add(self)
        db.session.commit()

        return token, self.auth_token_expire.strftime('%d/%m/%Y %H:%M:%S')

    def send_email(self, subject='', body=''):
        msg = Message(
            subject=subject,
            body=body,
            sender='sergiovenicio2015@gmail.com',
            recipients=[self.email,])

        return mail.send(msg)

    def __repr__(self):
        return f"ID: {self.id}, Email: {self.email}, Name: {self.name}"

