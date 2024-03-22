from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ics import Calendar
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

# Update this function as needed to process the .ics file and interests string
def process_calendar_and_interests(calendar_file, interests):
    # Placeholder for processing logic
    # Return a list of event names for demonstration
    return ["Event 1", "Event 2", "Event 3"]

@application.route('/find-events', methods=['POST'])
def find_events():
    if 'calendarFile' not in request.files:
        return redirect(request.url)
    file = request.files['calendarFile']
    interests = request.form['interests']
    
    if file.filename == '':
        return redirect(request.url)
    if file and interests:
        filename = secure_filename(file.filename)
        filepath = os.path.join('tmp', filename)  # Temporary save location
        file.save(filepath)

        with open(filepath, 'r') as f:
            calendar_content = f.read()
        calendar = Calendar(calendar_content)
        
        # Process the calendar and interests to get a list of events
        events = process_calendar_and_interests(calendar, interests)
        # Now pass the list of events to another template (e.g., events.html)
        
        return render_template('events.html', events=events)
    return redirect(url_for('home'))

@application.route('/api/ping_post', methods=['POST'])
def api_openai_request():
    json = request.json
    print(json)
    
    return jsonify({"success": True, "response": json})

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=False)