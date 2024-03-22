from calendar_import import ics_to_dict

# Path to the .ics file
ics_file_path = '../acorn_calendar.ics'

# Reading the content of the .ics file
try:
    with open(ics_file_path, 'r') as file:
        ics_data_from_file = file.read()
    success = True
except FileNotFoundError:
    success = False
    ics_data_from_file = ""

print(ics_data_from_file)

print(ics_to_dict(ics_data_from_file))


