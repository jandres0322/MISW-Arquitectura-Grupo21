from flask_restful import Resource
from ..modelos import db, Oferta, OfertaSchema, Empresa, EmpresaSchema
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker="redis://localhost:6379/0")

@celery_app.task(name="registrar_log")
def registrar_log(*args):
    pass

import traceback

oferta_schema = OfertaSchema()
empresa_Schema = EmpresaSchema()

    
class VistaOfertas(Resource):
    def get(self):
            return [oferta_schema.dump(oferta) for oferta in Oferta.query.all()]

    def post(self):
        try:
            titulo = request.json.get("titulo")
            descripcion = request.json.get("descripcion")
            lenguajes = request.json.get("lenguajes")
            empresa = request.json.get("empresa")
            nueva_oferta = Oferta(
                titulo=titulo,
                descripcion=descripcion,
                lenguajes=lenguajes,
                empresa=empresa
            )
            args = (titulo, datetime.utcnow())
            registrar_log.apply_async(args=args, queue="logs")
            db.session.add(nueva_oferta)
            db.session.commit()
            return oferta_schema.dump(nueva_oferta), 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Error al crear la oferta: {}".format(str(e))}, 500  