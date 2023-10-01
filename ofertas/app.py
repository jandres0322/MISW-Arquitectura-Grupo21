import requests
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/abc.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

jwt = JWTManager(app)
api = Api(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    titulo = db.Column(db.String(100))
    estado = db.Column(db.Integer)


class OfertaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "user", "titulo", "estado")

oferta_schema = OfertaSchema()
ofertas_schema = OfertaSchema(many=True)

class OfertaListResource(Resource):
    @jwt_required()
    def get(self):
        orders = Order.query.all()
        return ofertas_schema.dump(orders)

    @jwt_required()
    def post(self):
        headers = {'Authorization': request.headers['Authorization']}
        user = requests.get(f"https://users:5000/users/{request.json['user']}", verify=False, headers=headers)
        if user.status_code==200:
            new_offer = Order(
                user=request.json['user'],
                titulo=request.json['titulo'],
                estado=request.json['estado']
            )
            db.session.add(new_offer)
            db.session.commit()
            return oferta_schema.dump(new_offer)
        else:
            return {"error": "The offer or the user dont exist"}, 400


class OfertaEstado(Resource):
    @jwt_required()
    def get(self, oferta_id):
        offer = Order.query.get_or_404(oferta_id)
        return oferta_schema.dump(offer)
    
class CambiarEstado(Resource):
    @jwt_required()
    def put(self, oferta_id):
        offer = Order.query.get_or_404(oferta_id)
        new_estado = request.json.get('estado')

        if new_estado is not None:
            offer.estado = new_estado

            db.session.commit()

            return oferta_schema.dump(offer)
        else:
            return {"error": "El campo 'estado' es requerido en la solicitud JSON"}, 400


api.add_resource(OfertaListResource, '/oferta')
api.add_resource(OfertaEstado, '/oferta/<int:oferta_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')