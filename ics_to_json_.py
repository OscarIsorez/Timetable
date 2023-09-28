import json
import requests
from icalendar import Calendar
import os


"""
fonction qui prend en param?tre un lien qui pointe vers un fichier ics et qui retourne les �l�ments dans le format json
"""


def read_ics_file(url):
    response = requests.get(url)

    # V�rifier si la requete a r�ussi
    if response.status_code == 200:
        # Obtenir le contenu du fichier
        content = response.content

    return content



"""
    fonction qui prend en paramètre du contenu d'un fichier ics et qui retourne les éléments dans le format json

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
        return json.dumps({'error': str(e)}, indent=4)



"""
    fonction qui prend en paramètre un lien qui pointe vers un fichier ics et qui génère un fichier json  
"""
def generate_json_file(url, file_name):
    ics_content = read_ics_file(url)
    json_content = ics_to_json(ics_content)
    with open(file_name+".json", 'w') as f:
        f.write(json_content)


# ------

url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/o35ex53R.shu"

generate_json_file(url, "monfichier")