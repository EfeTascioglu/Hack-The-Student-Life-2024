from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/ping', methods=['GET'])
def api_ping():
    return jsonify({"success": True})
    

@app.route('/api/ping_post', methods=['POST'])
def api_openai_request():
    json = request.json
    return jsonify({"success": True, "response": json})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)