from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import os

DEBUG = True

def fetch_credentials(location="C:/Users/Efe/.AWS/credentials"):
    with open(location, 'r') as file:
        # Return the second line:
        return file.readlines()[1].strip().split(" = ")[1]

application = Flask(__name__)
if not DEBUG: application.config['SECRET_KEY'] = fetch_credentials()
CORS(application)

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/api/ping', methods=['GET'])
def api_ping():
    return jsonify({"success": True})
    

@application.route('/api/ping_post', methods=['POST'])
def api_openai_request():
    json = request.json
    print(json)
    
    return jsonify({"success": True, "response": json})

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80), debug=False))