import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/oferta', methods=['POST'])
def crear_oferta():
    try:
        data = request.get_json()
        response = requests.post("http://localhost:5001/ofertas",json=data)
        print(response)
        return response.json()
    except Exception as e:
        return jsonify(error=f'Error: {str(e)}'), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000)