from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mashmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/usuarios.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['JWT_SECRET_KEY'] = "secret-jwt"
app.config['JWT_ACCESS_TOKEN_EXPIRED'] = False

JWT = JWTManager(app)
api = Api(app)

class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(60))



class CandidatoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidato
        fields = ('id','nombre','username','password')

candito_schema = CandidatoSchema()
candidatos_schema = CandidatoSchema(many=True)


class CandidatoListResource(Resource):
    @jwt_required()
    def get(self):
        candidatos = candidato.query.all()
        return candidatos_schema.dump(candidatos)

    @jwt_required()
    def post(self):
        nuevo_candidato = Candidato(
            nombre = request.json['nombre'],
            username = request.json['username'],
            password = request.json['password']
        )
        db.session.add(nuevo_candidato)
        db.session.commit()
        return candidatos_schema.dump(nuevo_candidato)



class CandidatoResource(Resource):
    @jwt_required()
    def get(self,candidatoId):
        candidato = Candidato.query.get_or_404(candidatoId)
        return candidatos_schema.dump(candidato)


api.add_resource(CandidatoListResource, '/candidatos')
api.add_resource(CandidatoResource, '/candidatos/<int:candidatoId>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')

