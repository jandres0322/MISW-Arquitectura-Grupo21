from flask import Flask, request
import os
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("JWT_SECRET", "JF}]&p1CH4-?-k]")
app.config['JWT_TIME_EXPIRE'] = int(os.environ.get("JWT_EXPIRE_SECONDS", 120))


@app.route("/auth/candidato", methods=["POST"])
def autenticar_candidato():
    print("===== INIT AUTORIZADOR /auth/candidato =======")
    username = request.json["username"]
    payload = {
      "username": username,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=app.config['JWT_TIME_EXPIRE'])
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return {
       "token": token
    }, 200


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
