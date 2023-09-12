from icalendar import Calendar
from datetime import date, timedelta, datetime
import pyperclip
from random import randint
import requests
import os
# bibliothèque pour récupérer la date d'aujourd'hui et le jour de la semaine
import subprocess
import pytz


def convertir_heure_gmt_vers_locale(heure_gmt, pays):
    try:

        heure_gmt = str(heure_gmt)[0:-6]

        # Obtenez le fuseau horaire du pays spécifié
        fuseau_pays = pytz.timezone(pays)

        # Créez un objet datetime avec l'heure GMT
        heure_gmt = datetime.strptime(heure_gmt, '%Y-%m-%d %H:%M:%S')
        heure_gmt = pytz.utc.localize(heure_gmt)

        # Convertissez l'heure GMT en heure locale du pays
        heure_locale = heure_gmt.astimezone(fuseau_pays)

        return heure_locale
    except Exception as e:
        return f"Erreur : {str(e)}"


# L'URL du fichier que vous souhaitez télécharger
url = 'https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/m32jRq3k.shu'

# Envoyer une requête HTTP GET pour télécharger le fichier
response = requests.get(url)

acutal_date = date.today()

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Obtenir le contenu du fichier
    content = response.content

    # si le fichier Data.ics existe déjà on le supprime
    if os.path.exists("Data.ics"):
        os.remove("Data.ics")

    # Écrire le contenu dans un fichier .ics nommé "Data.ics"
    with open('Data.ics', 'wb') as file:
        file.write(content)

    print("Le fichier a été téléchargé avec succès et enregistré sous 'Data.ics'.")
else:
    print("La requête a échoué.")


# une liste de 50 strings de couleurs en hexadécimal dans la même gamme de couleurs
color_palette = ["#ffd6ff", "#f3ceff", "#e7c6ff", "#d8beff", "#c8b6ff", "#c0bbff", "#b8c0ff", "#bac8ff", "#baccff", "#bbd0ff", "#bbd6ff",
                 "#bbdaff", "#ffd6ff", "#f3ceff", "#e7c6ff", "#d8beff", "#c8b6ff", "#c0bbff", "#b8c0ff", "#bac8ff", "#baccff", "#bbd0ff", "#bbd6ff", "#bbdaff"]
backup_color_palette = color_palette.copy()


def count_events(week_data):
    all_events_text = []
    for event in week_data:
        all_events_text.append(event[2])
    return all_events_text

# fonction qui prend en paramètre la date d'aujou'dhui et qui renvoie le jour, le mois et l'année du lundi de la semaine dans laquelle se trouve la date d'aujourd'hui


def get_monday_date(date):
    # on récupère le jour de la semaine de la date d'aujourd'hui
    day = date.weekday()
    # si le jour est lundi, on renvoie la date d'aujourd'hui
    if day == 0:
        return date
    # sinon on renvoie la date d'aujourd'hui moins le nombre de jours qui sépare la date d'aujourd'hui du lundi de la semaine
    else:
        return date - timedelta(days=day)


# Chargez le fichier .ics
with open('Data.ics', 'rb') as f:
    cal = Calendar.from_ical(f.read())

# Créez un dictionnaire pour stocker les données par jour de la semaine
week_data = {'Monday': [], 'Tuesday': [],
             'Wednesday': [], 'Thursday': [], 'Friday': []}


# Parcourez les événements du calendrier
for event in cal.walk('vevent'):

    # on ne va traiter que les éléments qui ont une date comprise entre le lundi de la semaine acutelle et le vendredi de la semaine actuelle
    if event.get('dtstart').dt.date() >= get_monday_date(date.today()) and event.get('dtstart').dt.date() <= get_monday_date(date.today()) + timedelta(days=4):

        summary = event.get('summary')
        location = event.get('location')
        start_time = convertir_heure_gmt_vers_locale(
            event.get('dtstart').dt, 'Europe/Paris') + timedelta(hours=0.5)
        end_time = convertir_heure_gmt_vers_locale(
            event.get('dtend').dt, 'Europe/Paris') + timedelta(hours=0.5)

        # tests : affichage des dates et heures des événements et des summary
        print(
            f"start_time : {start_time} ; end_time : {end_time} ; summary : {summary}")
        # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
        day_of_week = start_time.strftime('%A')

        # Créez une chaîne de texte pour l'événement
        event_texts = f"{summary} ({location})"

        # Ajoutez l'événement au dictionnaire de données correspondant au jour de la semaine
        week_data[day_of_week].append((start_time, end_time, event_texts))

# Créez un tableau HTML
html_table = "<table border='1'>"
html_table += f"<tr><th>Plage Horaire</th><th style='border: none; background-color:{color_palette[0]};'>Lundi</th><th style='border: none;background-color: {color_palette[1]};'>Mardi</th><th style='border: none;background-color: {color_palette[2]};'>Mercredi</th><th style='border: none;background-color: {color_palette[3]};'>Jeudi</th><th  style='border: none;background-color: {color_palette[4]};'>Vendredi</th></tr>"

# Définissez l'heure de début (8h du matin, après avoir ajouté 2 heures)
start_hour = 8
start_minute = 0

# Définissez l'heure de fin (20h30 du soir, après avoir ajouté 2 heures)
end_hour = 18
end_minute = 30

# Parcourir les heures de 8h à 20h30 avec un intervalle de 15 minutes


# on utilisera la bibliothèque datetime pour créer un objet datetime
current_time = datetime(
    year=acutal_date.year, month=acutal_date.month, day=acutal_date.day, hour=start_hour, minute=start_minute)

# mettre les heures que une fois sur deux
one_or_two = True

liste_cours = []
liste_cours_uniques = []

# ----------------------------------GESTION DU CODE HTML--------------------------------------------


while current_time.hour < end_hour or (current_time.hour == end_hour and current_time.minute <= end_minute):
    html_table += "<tr>"

    # Calculer la plage horaire
    time_range_start = current_time.strftime('%H:%M')
    current_time += timedelta(minutes=15)
    time_range = f"{time_range_start}"

    # Mettre les heures sur 2 cellules, une fois sur deux
    if one_or_two:

        if color_palette != []:
            color = color_palette[0]
            color_palette.pop(0)
        else:
            color_palette = backup_color_palette.copy()
            color = color_palette[0]
            color_palette.pop(0)

        html_table += f"<td rowspan='2' style='border:none;background-color: {color}'>{time_range} --------</td>"
        one_or_two = False
    else:
        one_or_two = True

    # Parcourir les jours de la semaine
    for day, events in week_data.items():
        event_texts = []
        for event_start, event_end, event_desc in events:

            if event_start.time() <= current_time.time() < event_end.time():
                event_texts.append(event_desc)
        
        #on vérifie si event_texts[0][0:5] est déjà dans liste_cours et également si les dates de départ et de fin sont les mêmes
        if event_texts:
            if event_texts[0] not in liste_cours: # and events[0][0].date() == events[0][1].date():
                liste_cours.append(event_texts[0])
                rowspan = len(event_texts[0])
                event_desc = str(event_texts[0])
                # on enleve les espces dans le nom de la classe   
                n_classe = events[0][2][0:4].replace(" ", "")
                nbr_rowspan = (events[0][1] - events[0][0]) // timedelta(minutes=15)

                html_table += f"<td  rowspan='{nbr_rowspan} 'class='{n_classe}';>{event_desc}</td>"
                # Ignorer les lignes fusionnées suivantes pour ce cours
                # for _ in range(1, rowspan):
                #     html_table += "<tr></tr>"
        else:
            # Cellule vide
            html_table += "<td style='color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 10px;'>----------------------------------------</td>"

    html_table += "</tr>"

html_table += "</table>"

html_page = '<!DOCTYPE html><html lang="fr"><meta charset="UTF-8"><title>Emploi du temps</title><link rel="stylesheet" href="./style.css"><head>'
html_page += html_table
html_page += '</head><body></body></html>'


# ----------------------------GESTION DES FICHIERS--------------------------------------------


# on ne garde que les 4 premiers caractères de chaque élément de liste_cours
liste_cours = [x[0:4] for x in liste_cours]

# on supprime le fichier html s'il existe déjà
if os.path.exists("Timetable/index.html"):
    os.remove("Timetable/index.html")

# on crée un fichier html avec le contenu de html_page
fichier = open("Timetable/index.html", "w")
fichier.write(html_page)
fichier.close()


if os.path.exists("Timetable/style.css"):
    os.remove("Timetable/style.css")


# on crée un fichier css avec le contenu de style.css
fichier = open("Timetable/style.css", "w")
# pour chaque élément de liste_cours, on crée une classe css avec une couleur dans la liste color_palette

fichier.write("th, td {width: 15vw;}\n")
for i in range(len(liste_cours)):
    # print(liste_cours[i])
    # print(i)
    if liste_cours[i].count(' ') > 0:
        liste_cours[i] = liste_cours[i].replace(" ", "")
    fichier.write(
        f".{liste_cours[i]} {{background-color: {backup_color_palette[randint(0,len(backup_color_palette) -1)]}; border: none;border-radius: 10px;padding: 10px;}}\n")
fichier.close()


# -------------------------------------------------------------------------------------------


# dans le terminal de commande, on lance les commandes suivantes pour mettre à jour le site web
# cd Timetable/
# git add .
# git commit -m "update"
# git push


# Spécifiez le répertoire dans lequel vous souhaitez exécuter les commandes Git
repo_directory = 'C:/Users/Oscar/OneDrive/Documents/Timetable/Timetable'

# Commande Git : git add .
git_add_command = ['git', 'add', '.']

# Commande Git : git commit -m "update"
git_commit_command = ['git', 'commit', '-m', 'update']

# Commande Git : git push
git_push_command = ['git', 'push']

# Exécutez les commandes Git dans le répertoire du dépôt
try:
    subprocess.run(git_add_command, cwd=repo_directory, check=True)
    subprocess.run(git_commit_command, cwd=repo_directory, check=True)
    subprocess.run(git_push_command, cwd=repo_directory, check=True)
    print("Les commandes Git ont été exécutées avec succès.")
except subprocess.CalledProcessError as e:
    print("Une erreur s'est produite lors de l'exécution des commandes Git :", e)
