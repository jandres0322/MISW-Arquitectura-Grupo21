from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

db = SQLAlchemy()

class Oferta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    descripcion = db.Column(db.String(128))
    lenguajes = db.Column(db.String(128))
    empresa = db.Column(db.String(128))

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.descripcion, self.lenguajes, self.empresa)

class OfertaSchema(SQLAlchemySchema):
    class Meta:
        model = Oferta
        include_relationships = True
        load_instance = True
    id = fields.Integer()
    titulo = fields.String()
    descripcion = fields.String()
    lenguajes = fields.String()


