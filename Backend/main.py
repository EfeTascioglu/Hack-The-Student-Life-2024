from calendar_import import ics_to_dict
from ics import Calendar
import json

def load_ics_file(ics_file_path):
    # ics_file_path = '../acorn_calendar.ics'
    try:
        with open(ics_file_path, 'r', encoding="utf8") as file:
            ics_data = file.read()
    except FileNotFoundError:
        ics_data = ""
    return ics_data

def is_conflicting(event1, event2):
    """Check if two events conflict."""
    return not (event1.end <= event2.begin or event1.begin >= event2.end)

def find_non_conflicting_events(student_schedule, events_schedules):
    """Find events from the giant schedule that don't conflict with the student's schedule."""
    non_conflicting_events = []

    if not isinstance(events_schedules, list):
        events_schedules = [events_schedules]

    # Iterate over each event in the giant events schedule
    for events_schedule in events_schedules:
        for event in events_schedule.events:
            conflict_found = False
            
            # Check against each event in the student's schedule
            for student_event in student_schedule.events:
                if is_conflicting(event, student_event):
                    conflict_found = True
                    break  # Exit early if any conflict is found
            
            # If no conflicts were found, add to the non-conflicting events list
            if not conflict_found:
                non_conflicting_events.append(event)
    
    return non_conflicting_events

def filter_list_by_query(events_list, query=''):
    if query == '': return events_list


def pretty_print_schedule(schedule):
    reduced_events_json = json.dumps(schedule, indent=4)

    print(reduced_events_json)


if __name__ == '__main__':
    student_path = 'acorn_calendar.ics'
    student_text = load_ics_file(student_path)

    events_path = 'events_calendar.ics'
    events_text = load_ics_file(events_path)

    initial_student_schedule = ics_to_dict(student_text)

    #pretty_print_schedule(initial_student_schedule)

    # Example usage
    student_schedule = Calendar(student_text)
    events_schedule = Calendar(events_text)
    #events_schedule = Calendar(events_text)

    non_conflicting_events = find_non_conflicting_events(student_schedule, events_schedule)

    # Output or further process the non-conflicting events
    for event in non_conflicting_events:
        print(event)
