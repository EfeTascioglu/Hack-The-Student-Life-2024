from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import os
from openai import OpenAI

def fetch_credentials(dir='C:/Users/Efe/.openAI'):
    file_name = dir + '/credentials'
    with open(file_name, 'r') as f:
        lines = f.readlines()
        access_key_id = lines[1].split('=')[1].strip()
        secret_key = lines[2].split('=')[1].strip()
        return secret_key

client = OpenAI(api_key=fetch_credentials())
# Try to use GPT3.5-Turbo, then Baggage and Ada (which are about 4 times cheaper)
 # PUT YOUR OWN KEY HERE

def request_chat_gpt(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    #max_tokens=100,
    #'temperature=0.9,
    #top_p=1.0,
    #frequency_penalty=0.0,
    #presence_penalty=0.0,
    #stop=["\n", " Human:", " AI:"]
    )
    return completion.choices[0].message.content


application = Flask(__name__)
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
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=False)