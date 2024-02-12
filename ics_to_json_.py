import json
import requests
from icalendar import Calendar
import os


"""
    @param url: lien qui pointe vers un fichier ics
    @return content: contenu du fichier ics
"""
def read_ics_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
    return content



"""
    @param ics_content: contenu du fichier ics
    @return json_content: contenu du fichier ics converti en json
"""
def ics_to_json(ics_content): 
    try:
        cal = Calendar.from_ical(ics_content)
        events = []

        for event in cal.walk('vevent'):
            event_JSON = {
                'summary': str(event.get('summary', '')),
                'description': str(event.get('description', '')),
                'start': str(event.get('dtstart', '')),
                'end': str(event.get('dtend', '')),
                'location': str(event.get('location', '')),
            }
            events.append(event_JSON)

        return json.dumps(events, indent=4, ensure_ascii=False)

    except Exception as e:
        return json.dumps({'Error': str(e)}, indent=4)



"""
    @param url: lien qui pointe vers un fichier ics
    @param file_name: nom du fichier json à générer
    @return vide
"""
def generate_json_file(url, file_name):
    ics_content = read_ics_file(url)
    json_content = ics_to_json(ics_content)
    with open(file_name+".json", 'w') as f:
        f.write(json_content)

    


# ------MAIN------

url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/o35ex53R.shu"

generate_json_file(url, "monfichier")