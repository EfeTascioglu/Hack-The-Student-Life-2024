import json

ics_data = """
BEGIN:VCALENDAR
PRODID:-//Ben Fortuna//iCal4j 1.0//EN
VERSION:2.0
CALSCALE:GREGORIAN
BEGIN:VEVENT
DTSTAMP:20240322T160200Z
UID:b5b0d692-72e7-48fc-b51f-21f37345aafd
SUMMARY:CSC413H1 LEC2001
DTSTART;TZID=America/Toronto:20240109T130000
DTEND;TZID=America/Toronto:20240109T160000
STATUS:CONFIRMED
DESCRIPTION:Neural Networks and\nMechanical Engineering Bldg
LOCATION:MC 254
CREATED:20240322T160200Z
RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=20240405T235959
EXDATE;TZID=America/Toronto:20240220T130000
BEGIN:VALARM
TRIGGER:-PT1H
REPEAT:4
DURATION:PT15M
ACTION:DISPLAY
DESCRIPTION:Neural Networks and
END:VALARM
END:VEVENT
BEGIN:VEVENT
DTSTAMP:20240322T160200Z
UID:3cb4b670-a9d3-4087-8c19-a0d4dd360db3
SUMMARY:ECE324H1 LEC0101
DTSTART;TZID=America/Toronto:20240110T100000
DTEND;TZID=America/Toronto:20240110T110000
STATUS:CONFIRMED
DESCRIPTION:Machine Intelligence\, Software\nGalbraith Building
LOCATION:GB 304
CREATED:20240322T160200Z
RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=20240412T235959
EXDATE;TZID=America/Toronto:20240221T100000
BEGIN:VALARM
TRIGGER:-PT1H
REPEAT:4
DURATION:PT15M
ACTION:DISPLAY
DESCRIPTION:Machine Intelligence\, Software
END:VALARM
END:VEVENT
BEGIN:VEVENT
DTSTAMP:20240322T160200Z
UID:0480b7cb-f69c-496a-a8c2-b99008db691c
SUMMARY:ECE324H1 LEC0101
DTSTART;TZID=America/Toronto:20240111T160000
DTEND;TZID=America/Toronto:20240111T180000
STATUS:CONFIRMED
DESCRIPTION:Machine Intelligence\, Software\nWallberg Building
LOCATION:WB 116
CREATED:20240322T160200Z
RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=20240412T235959
EXDATE;TZID=America/Toronto:20240222T160000
BEGIN:VALARM
TRIGGER:-PT1H
REPEAT:4
DURATION:PT15M
ACTION:DISPLAY
DESCRIPTION:Machine Intelligence\, Software
END:VALARM
END:VEVENT
BEGIN:VEVENT
DTSTAMP:20240322T160200Z
UID:67d12f74-5b7c-4f14-97e6-96743c4a2e53
SUMMARY:ECE324H1 TUT0101
DTSTART;TZID=America/Toronto:20240109T100000
DTEND;TZID=America/Toronto:20240109T110000
STATUS:CONFIRMED
DESCRIPTION:Machine Intelligence\, Software\nBAHEN CENTRE FOR INFORMATION TECH
LOCATION:BA 2139
CREATED:20240322T160200Z
RRULE:FREQ=WEEKLY;WKST=MO;UNTIL=20240412T235959
EXDATE;TZID=America/Toronto:20240220T100000
BEGIN:VALARM
TRIGGER:-PT1H
REPEAT:4
DURATION:PT15M
ACTION:DISPLAY
DESCRIPTION:Machine Intelligence\, Software
END:VALARM
END:VEVENT
END:VCALENDAR
"""



# Adjusting the parsing logic to handle lines without a colon and multi-line values

def parse_ics(ics_content):
    events = []
    event = None
    last_key = None
    for line in ics_content.splitlines():
        line = line.strip()
        if line == "BEGIN:VEVENT":
            event = {}
            last_key = None
        elif line == "END:VEVENT":
            events.append(event)
            event = None
            last_key = None
        elif event is not None:
            if ':' in line:
                key, value = line.split(':', 1)
                last_key = key
                # Special handling for keys with parameters like DTSTART;TZID=America/Toronto
                if ";" in key:
                    key, _ = key.split(";", 1)
                # Handle multiple occurrences of the same key (like EXDATE)
                if key in event:
                    if isinstance(event[key], list):
                        event[key].append(value)
                    else:
                        event[key] = [event[key], value]
                else:
                    event[key] = value
            elif last_key:  # Continuation of a previous line (e.g., a description spanning multiple lines)
                event[last_key] += line

    return events



def ics_to_dict(ics_content):
    events_list = parse_ics(ics_content)
    events_dict = {event["UID"]: event for event in events_list}
    reduced_events_dict = {}
    for uid, event in events_dict.items():
        reduced_events_dict[uid] = {
            "DESCRIPTION": event.get("DESCRIPTION", ""),
            "LOCATION": event.get("LOCATION", ""),
            "DTSTART": event.get("DTSTART", ""),
            "DTEND": event.get("DTEND", ""),
            "RRULE": event.get("RRULE", ""),
            "EXDATE": event.get("EXDATE", [])
        }
    return reduced_events_dict



if __name__ == "__main__":
    # Re-parsing the .ics content with the adjusted logic
    events_list = parse_ics(ics_data)

    # Converting the list of events to a dictionary, indexed by UID
    events_dict = {event["UID"]: event for event in events_list}

    print(events_dict)

    reduced_events_dict = {}

    for uid, event in events_dict.items():
        reduced_events_dict[uid] = {
            "DESCRIPTION": event.get("DESCRIPTION", ""),
            "LOCATION": event.get("LOCATION", ""),
            "DTSTART": event.get("DTSTART", ""),
            "DTEND": event.get("DTEND", ""),
            "RRULE": event.get("RRULE", ""),
            "EXDATE": event.get("EXDATE", [])
        }

    # print(reduced_events_dict)

    # Converting the Python dictionary to JSON
    reduced_events_json = json.dumps(reduced_events_dict, indent=4)

    # just for prettier printed visualization. we will just use the dict, not the json
    reduced_events_json = json.dumps(ics_to_dict(ics_data), indent=4)

    print(reduced_events_json)