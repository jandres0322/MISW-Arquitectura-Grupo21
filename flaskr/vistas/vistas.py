from flask_restful import Resource
from ..modelos import db, Oferta, OfertaSchema, Empresa, EmpresaSchema
from flask import request
from sqlalchemy.exc import IntegrityError

import logging

oferta_schema = OfertaSchema()
empresa_Schema = EmpresaSchema()

class VistaEmpresa(Resource):   
    def get(self):
        return [empresa_Schema.dump(empresa) for empresa in Empresa.query.all()]
     
    def post(self):
        nuevo_usuario = Empresa(nombre=request.json["nombre"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return 'Empresa creada exitosamente', 201

    def put(self, id_empresa):
        empresa = Empresa.query.get_or_404(id_empresa)
        db.session.commit()
        return empresa_Schema.dump(empresa)

    def delete(self, id_empresa):
        empresa = Empresa.query.get_or_404(id_empresa)
        db.session.delete(empresa)
        db.session.commit()
        return 'Operacion exitosa',204
    
class VistaOfertasEmpresa(Resource):
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

            db.session.add(nueva_oferta)
            db.session.commit()

            return oferta_schema.dump(nueva_oferta), 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Error al crear la oferta: {}".format(str(e))}, 500  