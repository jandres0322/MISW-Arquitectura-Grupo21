from flaskr import create_app
from .modelos import db, Empresa, Oferta
from .modelos import OfertaSchema
from flask_restful import Api
from .vistas import VistaOfertas, VistaOferta, VistaEmpresa, VistaOfertasEmpresa

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#PRUEBAS
# with app.app_context():

    # prueba para crear una empresa---------------------------------------------------------------------------------
    # e = Empresa(nombre='Torre')
    # db.session.add(e)
    # db.session.commit()

    # prueba para crear una oferta de una empresa-------------------------------------------------------------------
    # e = Empresa(nombre='Torre')
    # o = Oferta( titulo='Oferta1', descripcion='Descipcon de la oferta labolar', lenguajes='Python')
    # e.ofertas.append(o)
    # db.session.add(e)
    # db.session.commit()
    # print(Empresa.query.all())
    # print(Empresa.query.all()[0].ofertas)

    # prueba de serialización de la base de datos--------------------------------------------------------------------
    # oferta_schema = OfertaSchema()
    # O = Oferta( titulo='Oferta2', descripcion='Descipcon de la oferta labolar', lenguajes='Java')
    # db.session.add(O)
    # db.session.commit()
    # print([oferta_schema.dump(oferta) for oferta in Oferta.query.all()])

#  api---------------------------------

api = Api(app)
api.add_resource(VistaOfertas, '/ofertas')
api.add_resource(VistaOferta, '/oferta/<int:id_oferta>')
api.add_resource(VistaEmpresa, '/empresa')
api.add_resource(VistaOfertasEmpresa, '/ofertasempresa/<int:id_empresa>')
