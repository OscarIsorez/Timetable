import json
import requests
import icalendar

"""

fonction qui prend en param?tre un lien qui pointe vers un fichier ics et qui retourne les éléments dans le format json
"""


def read_ics_file(url):
    response = requests.get(url)

    # Récupérer la date d'aujourd'hui
    acutal_date = date.today()

    # Vérifier si la requete a réussi
    if response.status_code == 200:
        # Obtenir le contenu du fichier
        content = response.content

        script_directory = os.path.dirname(__file__)
        # si le fichier n'existe pas, on le crée dans le meme répertoire que le script

        if not os.path.exists(os.path.join(script_directory, f"Data.ics")):
            with open(os.path.join(script_directory, f"Data.ics"), "w") as fichier:
                fichier.write("")

        # Chemin complet du fichier
        chemin_fichier = os.path.join(script_directory, f"Data.ics")

        # écriture du contenu dans le fichier
        with open(chemin_fichier, "wb") as fichier:
            fichier.write(content)
        # print("Le fichier a été téléchargé avec succ?s et enregistré sous 'Data.ics'.")

    else:
        print("La requete a échoué.")

    # Obtenir le répertoire du script

    script_directory = os.path.dirname(__file__)

    # Construire le chemin relatif vers le fichier "Data.ics"

    fichier_relative_path = os.path.join(script_directory, "Data.ics")

    # Vérifier si le fichier existe
    if os.path.exists(fichier_relative_path):

        # Ouvrir le fichier en lecture
        with open(fichier_relative_path, "r", encoding="iso-8859-2") as f:
            cal = Calendar.from_ical(f.read())

    else:   
        print("Le fichier 'Data.ics' n'existe pas dans le répertoire du script.")


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

# ------


url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/o35ex53R.shu"
