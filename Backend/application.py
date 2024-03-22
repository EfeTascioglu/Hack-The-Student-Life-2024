from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ics import Calendar
from calendar_utils import load_ics_file, find_non_conflicting_events, parse_text
from calendar_import import ics_to_dict
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

DEBUG = True
client = None if DEBUG else OpenAI(api_key=fetch_credentials(dir='C:/Users/Efe/.openAI'))
# Try to use GPT3.5-Turbo, then Baggage and Ada (which are about 4 times cheaper)
 # PUT YOUR OWN KEY HERE

def request_chat_gpt(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


application = Flask(__name__)
CORS(application)

def find_activities_that_are_relevant(events, interests):
    prompt = "A student has a list of interests and wants a list of events that are relevant to them. Take the following interests:\n" + str(interests) + "\nAnd the following list of events:\n" + str(events) + "\nReturn the indices of events that are most relevant to the student's interests as a comma seperated list. Return At least 9 Values. Order them from most relevant of interests to least relevant. Do not return anything else. Do not explain your work. Return example: 0,4,6,9"
    return_val = request_chat_gpt(prompt)
    print(return_val)
    return_val = return_val.split(",")
    for i in range(len(return_val)):
        return_val[i] = int(return_val[i].strip())
    return return_val

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

def process_events_to_descriptions(events, reduced_events_dict):
    events_out = []
    for event in events:
        # Assuming `event` has an attribute `uid` that matches keys in `reduced_events_dict`
        uid = getattr(event, 'uid', None)
        if uid and uid in reduced_events_dict:
            event_info = reduced_events_dict[uid]
            events_out.append({
                "name": getattr(event, 'name', ''),
                "begin": getattr(event, 'begin', '').isoformat() if getattr(event, 'begin', None) else '',
                "end": getattr(event, 'end', '').isoformat() if getattr(event, 'end', None) else '',
                "description": event_info.get("DESCRIPTION", "")
            })
    return events_out

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

        student_text = load_ics_file(filepath)

        events_text = load_ics_file('static/events/events_calendar.ics')

        events_dict = ics_to_dict(events_text)
        
        print('event text', events_text)
        student_schedule = parse_text(student_text)
        events_schedule = parse_text(events_text)
        non_conflicting_events = find_non_conflicting_events(student_schedule, events_schedule)

        non_conflicting_events = find_non_conflicting_events(student_schedule, events_schedule)

        # Process non-conflicting events to get descriptions
        processed_events = process_events_to_descriptions(non_conflicting_events, events_dict)

        events = processed_events

        

        # ChatGPT
        if not DEBUG:
            event_indices = find_activities_that_are_relevant(events, interests)

            print('testing', event_indices)

            events_out = []
            for i, event in enumerate(events):
                if i in event_indices:
                    dict_thing = {
                        'name': event.name,
                        'description': 'haaa',
                    }
                    events_out.append(event.name)

            events = events_out
        else:
            events_out = []
            for i, event in enumerate(events):
                events_out.append(event)

            events = events_out
        
        # Process the calendar and interests to get a list of events
        #events = process_calendar_and_interests(calendar, interests)
        # Now pass the list of events to another template (e.g., events.html)

        return render_template('index.html', events=events)
    return redirect(url_for('home'))

@application.route('/api/ping_post', methods=['POST'])
def api_openai_request():
    json = request.json
    print(json)
    
    return jsonify({"success": True, "response": json})

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)), debug=False)