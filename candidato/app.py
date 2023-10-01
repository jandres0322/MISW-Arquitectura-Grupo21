from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
#from flask_mashmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_migrate import Migrate
import os
import hashlib




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidatos.sqlite'
db = SQLAlchemy(app)
#ma = Marshmallow(app)
app.config['JWT_SECRET_KEY'] = "secret-jwt"
app.config['JWT_ACCESS_TOKEN_EXPIRED'] = False
with app.app_context():
    db.create_all()

migrate = Migrate(app,db)
JWT = JWTManager(app)
api = Api(app)

class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(60))



class CandidatoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Candidato
        fields = ('id','nombre','username','password')

candidato_schema = CandidatoSchema()
candidatos_schema = CandidatoSchema(many=True)


class CandidatoListResource(Resource):
    #@jwt_required()
    def get(self):
        candidatos = Candidato.query.all()
        return candidatos_schema.dump(candidatos)

    #@jwt_required()
    def post(self):
        nombre = request.json.get("nombre")
        username = request.json.get("username")
        password = request.json.get("password")

        salt = os.urandom(32)
        password_bytes = password.encode("utf-8")
        salted_password = salt + password_bytes
        hashed_password = hashlib.sha256(salted_password).hexdigest()

        nuevo_candidato = Candidato(
            nombre=nombre,
            username=username,
            password=hashed_password
        )
        db.session.add(nuevo_candidato)
        db.session.commit()
        return candidato_schema.dump(nuevo_candidato)



class CandidatoResource(Resource):
    #@jwt_required()
    def get(self, username):
        candidato = Candidato.query.filter_by(username = username).first()
        if candidato:
            return candidatos_schema.dump(candidato)
        else :
            return 'candidato no encontrado', 404





api.add_resource(CandidatoListResource, '/candidatos')
api.add_resource(CandidatoResource, '/candidatos/<string:username>')

#if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5003)))