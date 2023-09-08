from flask_restful import Resource
from ..modelos import db, Oferta, OfertaSchema, Empresa, EmpresaSchema
from flask import request
from sqlalchemy.exc import IntegrityError

oferta_schema = OfertaSchema
empresa_Schema = EmpresaSchema

class VistaOfertas(Resource):

    def get(self):
        return [oferta_schema.dump(oferta) for oferta in Oferta.query.all()]
    
    def post(self):
        nueva_oferta = Oferta(titulo=request.json['titulo'],\
                              descripcion=request.json['descripcion'],\
                                lenguajes=request.json['lenguajes'],\
                                empresa=request.json['empresa']
                                )
        db.session.add(nueva_oferta)
        db.session.commit()
        return oferta_schema.dump(nueva_oferta)
    
class VistaOferta(Resource):

    def get(self, id_oferta):
        return(oferta_schema.dump(Oferta.query.get_or_404(id_oferta)))
    
    def put(self, id_oferta):
        oferta = Oferta.query.get_or_404(id_oferta)
        oferta.titulo = request.json.get('titulo', oferta.titulo)
        oferta.descripcion = request.json.get('descripcion', oferta.descripcion)
        oferta.lenguajes = request.json.get('lenguajes', oferta.lenguajes)
        db.session.commit()
        return oferta_schema.dump(oferta)


# class VistaEmpresas(Resource):

#     def get(self):
#         return [empresa_Schema.dump(empresa) for empresa in Empresa.query.all()]
    
#     def post(self):
#         nueva_empresa = Oferta(nombre=request.json['nombre'])
#         db.session.add(nueva_empresa)
#         db.session.commit()
#         return oferta_schema.dump(nueva_empresa)
    
# class VistaEmpresa(Resource):

#     def get(self, id_empresa):
#         return(oferta_schema.dump(Oferta.query.get_or_404(id_empresa)))
    
#     def put(self, id_empresa):
#         empresa = Oferta.query.get_or_404(id_empresa)
#         empresa.nombre = request.json.get('nombre', empresa.nombre)
#         db.session.commit()
#         return oferta_schema.dump(empresa)
    

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
        return '',204
    
class VistaOfertasEmpresa(Resource):
    def post(self, id_empresa):
        try:
            nuevo_oferta = Oferta(
                titulo=request.json["titulo"],
                descripcion=request.json["descripcion"],
                lenguajes=request.json["lenguajes"],
                # empresa=request.json[id_empresa]
            )
            # empresa = Empresa.query.get_or_404(id_empresa)
            # empresa.ofertas.append(nuevo_oferta)
            db.session.add(nuevo_oferta)  

            db.session.commit()
            return oferta_schema.dump(nuevo_oferta), 201  

        except IntegrityError:
            db.session.rollback()
            return {'message': 'El usuario ya tiene una oferta con los mismos datos'}, 409

# class VistaOfertasEmpresa(Resource):

#     def post(self, id_empresa):
#         try:
#             titulo = request.json.get("titulo")
#             descripcion = request.json.get("descripcion")
#             lenguajes = request.json.get("lenguajes")
#             empresa = request.json.get("empresa") 

#             nueva_oferta = Oferta(
#                 titulo=titulo,
#                 descripcion=descripcion,
#                 lenguajes=lenguajes,
#                 empresa=empresa
#             )

#             db.session.add(nueva_oferta)
#             db.session.commit()

#             return oferta_schema.dump(nueva_oferta), 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Error al crear la oferta: {}".format(str(e))}, 500 

    def get(self, id_empresa):
        empresa = Empresa.query.get_or_404(id_empresa)
        ofertas = empresa.ofertas
        return [oferta_schema().dump(oferta) for oferta in ofertas]

