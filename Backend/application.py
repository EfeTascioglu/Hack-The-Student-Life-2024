from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os

def fetch_credentials(location="C:/Users/Efe/.AWS/credentials"):
    with open(location, 'r') as file:
        # Return the second line:
        return file.readlines()[1].strip().split(" = ")[1]

application = Flask(__name__)
application.config['SECRET_KEY'] = fetch_credentials()
CORS(application)

@application.route('/api/ping', methods=['GET'])
def api_ping():
    return jsonify({"success": True})
    

@application.route('/api/ping_post', methods=['POST'])
def api_openai_request():
    json = request.json
    print(json)
    
    return jsonify({"success": True, "response": json})

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=False)