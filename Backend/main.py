from calendar_import import ics_to_dict
import json

def load_ics_file(ics_file_path):
    # ics_file_path = '../acorn_calendar.ics'
    try:
        with open(ics_file_path, 'r') as file:
            ics_data = file.read()
        success = True
    except FileNotFoundError:
        success = False
        ics_data = ""
    return ics_data

def pretty_print_schedule(schedule):
    reduced_events_json = json.dumps(schedule, indent=4)

    print(reduced_events_json)


if __name__ == '__main__':
    ics_file_path = '../acorn_calendar.ics'

    initial_student_schedule = ics_to_dict(load_ics_file(ics_file_path))

    pretty_print_schedule(initial_student_schedule)
