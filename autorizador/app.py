from flask import Flask, jsonify, request
import os


app = Flask(__name__)

@app.route('/api_gateway/auth', methods=['POST'])
def validate_permissions():
  try:
    data = request.get_json()
    print("Prueba -->", data)
  except Exception as e:
    print("Error -->", e)
  
if __name__ == "__main__":
  app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
  )
