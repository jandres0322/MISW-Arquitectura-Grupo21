from flask import Flask, request, jsonify
from functools import wraps
import jwt
import os
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("JWT_SECRET", "JF}]&p1CH4-?-k]")


HOST_AUTH = os.environ.get("HOST_AUTH", "http://localhost:5002")
HOST_CANDIDATOS = os.environ.get("HOST_CANDIDATOS", "http://localhost:5003")
HOST_OFERTAS = os.environ.get("HOST_OFERTAS", "http://localhost:5004")


def verificar_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token faltante'}), 401
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        request.current_user = payload
        return f(*args, **kwargs)

    return decorator


@app.route("/api/candidato/login", methods=["POST"])
def login_candidato():
    print("===== INIT API GATEWAY LOGIN CANDIDATO /api/candidato/login =======")
    ## Extraer información del cliente
    bodyRequest = request.json
    ## Validar información del candidato
    username = bodyRequest["username"]
    # response_candidato = requests.get(
    #     f"{HOST_CANDIDATOS}/candidatos/${username}"
    # )
    ## Generar token de autenticación
    response_auth = requests.post(
        f"{HOST_AUTH}/auth/candidato",
        json={
            "username": bodyRequest["username"],
            "password": bodyRequest["password"]
        }
    )
    ## Retornar token de autenticación
    response_auth_json = response_auth.json()
    return {
        "token": response_auth_json["token"]
    }, 200

@app.route("/api/ofertas/listar", methods=["GET"])
@verificar_token
def obtener_ofertas():
    bodyRequest = request.json
    id_ofertas = bodyRequest["ofertas"]
    if id_ofertas is None or len(id_ofertas) == 0:
        return {
            "mensaje": "El candidato no tiene ofertas"
        }, 404
    response_ofertas = requests.get(
        f"{HOST_OFERTAS}/ofertas",
        json={
            "ofertas":id_ofertas
        }
    )
    ofertas = response_ofertas.json["ofertas"]
    return {
        "mensaje": "Ofertas encontradas exitosamente",
        "ofertas": ofertas
    }, 200

@app.route("/api/ofertas/cambiar-estado/<id_oferta>", methods=["PUT"])
@verificar_token
def cambiar_estado_oferta(id_oferta):
    return {
        "message": "ENDPOINT Modificar Oferta",
        "id_oferta": id_oferta
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
