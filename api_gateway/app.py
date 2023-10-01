from flask import Flask, request, jsonify
from functools import wraps
import jwt
import os
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("JWT_SECRET", "JF}]&p1CH4-?-k]")


HOST_CANDIDATO = os.environ.get("HOST_CANDIDATO", "http://localhost:5002")
HOST_AUTH = os.environ.get("HOST_AUTH", "http://localhost:5004")


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
    print("===== INIT API GATEWAY /api/candidato/login =======")
    bodyRequest = request.json
    print(bodyRequest)
    # response_candidato = requests.post(
    #    f"{HOST_CANDIDATO}/candidato",
    #    json=bodyRequest
    # )
    # print(response_candidato)
    response_generar_token = requests.post(
        f"{HOST_AUTH}/auth/candidato",
        json={
            "username": bodyRequest["username"]
        }
    )
    response_generar_token_json = response_generar_token.json()
    return {
        "token": response_generar_token_json["token"]
    }, 200

@app.route("/api/ofertas", methods=["GET"])
@verificar_token
def obtener_ofertas():
    return {
        "message": "ENDPOINT Ver Ofertas"
    }

@app.route("/api/ofertas/<id_oferta>", methods=["PUT"])
@verificar_token
def modificar_estado_oferta(id_oferta):
    return {
        "message": "ENDPOINT Modificar Oferta",
        "id_oferta": id_oferta
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
