from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100))
    titulo = db.Column(db.String(100))
    candidato = db.Column(db.Integer())
    estado = db.Column(db.Integer())

class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "empresa", "titulo", "estado")