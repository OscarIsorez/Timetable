import json
import urllib.request
import icalendar

"""

fonction qui prend en param?tre un lien qui pointe vers un fichier ics et qui retourne les �l�ments dans le format json
"""

def read_ics_file(url):
    try:
        with urllib.request.urlopen(url) as response:
            # Lire le contenu en utilisant l'encodage iso-8859-2
            ics_content = response.read().decode('iso-8859-2')
            return ics_content
    except Exception as e:
        return json.dumps({'error': str(e)}, indent=4)

def ics_to_json(ics_content):
    try:
        cal = icalendar.Calendar.from_ical(ics_content)
        events = []

        for event in cal.walk('vevent'):
            event_data = {
                'summary': str(event.get('summary', '')),
                'description': str(event.get('description', '')),
                'start': str(event.get('dtstart', '')),
                'end': str(event.get('dtend', '')),
                'location': str(event.get('location', '')),
            }
            events.append(event_data)

        return json.dumps(events, indent=4, ensure_ascii=False).encode('iso-8859-2').decode('iso-8859-2')

    except Exception as e:
        return json.dumps({'error': str(e)}, indent=4)

def generate_json_file(url, file_name):
    ics_content = read_ics_file(url)
    json_content = ics_to_json(ics_content)
    with open(file_name, 'w', encoding='iso-8859-2') as f:
        f.write(json_content)

#------

url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/o35ex53R.shu"

