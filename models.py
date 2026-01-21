from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))

    lancamentos = db.relationship('Lancamento', backref='usuario', lazy=True)

class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    categoria = db.Column(db.String(50))
    valor = db.Column(db.Float)
    data = db.Column(db.Date, default=date.today)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
