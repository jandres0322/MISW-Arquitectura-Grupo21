from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields

db = SQLAlchemy()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(128))
    ofertas = db.relationship('Oferta', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return "{}".format(self.nombre)

class Oferta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    descripcion = db.Column(db.String(128))
    lenguajes = db.Column(db.String(128))
    empresa = db.Column(db.Integer, db.ForeignKey(Empresa.id))

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.descripcion, self.lenguajes, self.empresa)
    
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class OfertaSchema(SQLAlchemySchema):
    class Meta:
        model = Oferta
        include_relationships = True
        load_instance = True
    id = fields.Integer()
    titulo = fields.String()
    descripcion = fields.String()
    lenguajes = fields.String()
    

