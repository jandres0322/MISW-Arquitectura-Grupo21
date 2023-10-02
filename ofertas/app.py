from flask import Flask, request
from flask_restful import Api, Resource
from models import db, OrderSchema, Order
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ofertas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

oferta_schema = OrderSchema()
ofertas_schema = OrderSchema(many=True)


class OfertaListResource(Resource):
    def get(self):
        candidato = request.json["candidato"]
        orders = Order.query.filter_by(candidato = candidato).all()
        return ofertas_schema.dump(orders)

    def post(self):
        new_offer = Order(
            titulo=request.json['titulo'],
            empresa=request.json['empresa'],
            candidato=request.json['candidato'],
            estado=request.json['estado']
        )
        db.session.add(new_offer)
        db.session.commit()
        return oferta_schema.dump(new_offer)


class OfertaResource(Resource):

    def put(self, oferta_id):
        offer = Order.query.get_or_404(oferta_id)
        print("request.json", request.json)
        new_estado = request.json.get('estado')

        if new_estado is not None:
            offer.estado = new_estado
            db.session.commit()
            return oferta_schema.dump(offer)
        else:
            return {"error": "El campo 'estado' es requerido en la solicitud JSON"}, 400


api.add_resource(OfertaListResource, '/ofertas')
api.add_resource(OfertaResource, '/ofertas/cambiar-estado/<oferta_id>')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5004)))
