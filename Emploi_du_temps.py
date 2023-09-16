from icalendar import Calendar
from datetime import date, timedelta, datetime
import pyperclip
from random import randint
import requests
import os
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


""" 
    fonction qui prend en paramètre la liste des événements de la semaine et
    qui renvoie la liste des textes des événements de la semaine
"""


def count_events(week_data):
    all_events_text = []
    for event in week_data:
        all_events_text.append(event[2])
    return all_events_text


""" 
    fonction qui prend en paramètre la date d'aujourd'hui et
    qui renvoie la date du lundi de la semaine dans laquelle se trouve la date d'aujourd'hui
"""


def get_monday_date(date):
    # on récupère le jour de la semaine de la date d'aujourd'hui
    day = date.weekday()
    # si le jour est lundi, on renvoie la date d'aujourd'hui
    if day == 0:
        return date
    # sinon on renvoie la date d'aujourd'hui moins le nombre de jours qui sépare la date d'aujourd'hui du lundi de la semaine
    else:
        return date - timedelta(days=day)


"""
    fonction qui initialise le dictionnaire week_data avec les événements de la semaine
    Exemple : week_data = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
"""


def treat_data(date_to_treat):

    # Créez un dictionnaire pour stocker les données par jour de la semaine
    week_data = {'Monday': [], 'Tuesday': [],
                 'Wednesday': [], 'Thursday': [], 'Friday': []}

    # Parcourez les événements du calendrier
    for event in cal.walk('vevent'):
        # si la date dstat est comprise entre date_to_treat et date_to_treat + 4 jours
        if event.get('dtstart').dt.date() >= date_to_treat and event.get('dtstart').dt.date() <= date_to_treat + timedelta(days=4):
            # if event.get('dtstart').dt.date() >= date_to_treat and event.get('dtstart').dt.date() <=date_to_treat + timedelta(days=4):
            # print("date_to_treat", date_to_treat)
            # print("date_to_treat+4", date_to_treat + timedelta(days=4))

            # Obtenez les informations de l'événement
            summary = event.get('summary')
            location = event.get('location')
            start_time = convertir_heure_gmt_vers_locale(
                event.get('dtstart').dt, 'Europe/Paris') + timedelta(hours=0.5)
            end_time = convertir_heure_gmt_vers_locale(
                event.get('dtend').dt, 'Europe/Paris') + timedelta(hours=0.5)

            # tests : affichage des dates et heures des événements et des summary
            # print(
            #     f"start_time : {start_time} ; end_time : {end_time} ; summary : {summary}")
            # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
            day_of_week = start_time.strftime('%A')

            # Créez une chaîne de texte pour l'événement
            event_texts = f"{summary} ({location})"

            # Ajoutez l'événement au dictionnaire de données correspondant au jour de la semaine
            week_data[day_of_week].append((start_time, end_time, event_texts))

            # on affiche tous les event_texts dans la console
    return week_data


def generate_html_page(date_to_treat, color_palette, file_name, to_page):

    week_data = treat_data(date_to_treat)

    # Créez un tableau HTML
    html_table = ""
    html_table += "<table border='1'>"

    top_left = str(date_to_treat.day) + " \nau " + str((date_to_treat + timedelta(days=4)).day) + " 0" + \
        str((date_to_treat + timedelta(days=4)).month) + \
        "-" + str((date_to_treat + timedelta(days=4)).year)
    html_table += f"<tr><th class='first_column'>Semaine du {top_left}</th><th style='border: none; background-color:{color_palette[0]};'>Lundi</th><th style='border: none;background-color: {color_palette[1]};'>Mardi</th><th style='border: none;background-color: {color_palette[2]};'>Mercredi</th><th style='border: none;background-color: {color_palette[3]};'>Jeudi</th><th  style='border: none;background-color: {color_palette[4]};'>Vendredi</th></tr>"

    # Définissez l'heure de début (8h du matin, après avoir ajouté 2 heures)
    start_hour = 8
    start_minute = 0

    # Définissez l'heure de fin (20h30 du soir, après avoir ajouté 2 heures)
    end_hour = 19
    end_minute = 0

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
                color_palette.append(color)
            else:
                color_palette = backup_color_palette.copy()
                color = color_palette[0]
                color_palette.pop(0)
                color_palette.append(color)

            html_table += f"<td rowspan='2'class='first_column' style='text-align: right;border:none;background-color: {color}'> {'   ' +  str(time_range) + '   '}  </td>"
            one_or_two = False
        else:
            one_or_two = True

        # Parcourir les jours de la semaine
        for day, events in week_data.items():
            event_informations = []
            for event_start, event_end, event_desc in events:

                if event_start.time() <= current_time.time() < event_end.time():
                    event_informations.append(
                        [event_desc, event_start, event_end])

            # on vérifie si event_informations[0][0:5] est déjà dans liste_cours et également si les dates de départ et de fin sont les mêmes
            if event_informations:
                if event_informations[0] not in liste_cours:
                    liste_cours.append(event_informations[0])
                    event_desc = str(event_informations[0][0])
                    # on enleve les espces dans le nom de la classe
                    n_classe = event_informations[0][0][0:4].replace(" ", "")
                    nbr_rowspan = (
                        event_informations[0][2] - event_informations[0][1]) // timedelta(minutes=15)
                    html_table += f"<td  rowspan='{nbr_rowspan} 'class='{n_classe}';>{event_desc}</td>"

            else:
                # Cellule vide
                html_table += "<td class='empty'>----------------------------------------</td>"

        html_table += "</tr>"

    html_table += "</table>"

    html_page = f'<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><title>Emploi du temps</title><link rel="stylesheet" href="./{file_name}.css"></head><body>    '
    html_page += html_table
    html_page += f'<button id="bouton-suivant" onclick="window.location.href=\'./{to_page}.html\'">Swtich semaine</button>'
    html_page += '</body></html>'

    return html_page, liste_cours, liste_cours_uniques, color_palette, backup_color_palette


# ----------------------------GESTION DES FICHIERS--------------------------------------------

def generate_html_file_and_css_file(html_page, liste_cours, liste_cours_uniques, color_palette, backup_color_palette, file_name):
    # liste_cours contient des tableaux de 2 éléments. on souhaite garder uniquement les 4 premiers caractères de l'élément 0
    for i in range(len(liste_cours)):
        liste_cours[i][0] = liste_cours[i][0][0:4]

    # on supprime les doublons de liste_cours
    # la liste contenant elle meme des listes, on ne gardera que le premier élément de chaque élément
    liste_cours_uniques = []
    for i in range(len(liste_cours)):
        liste_cours_uniques.append(liste_cours[i][0])
    liste_cours_uniques = list(set(liste_cours_uniques))


# --------------------------------------------HTML-----------------------------------------------

    # on supprime le fichier html s'il existe déjà
    # Obtenir le répertoire du script
    script_directory = os.path.dirname(__file__)

    # Chemin complet du fichier "index.html"
    chemin_fichier = os.path.join(script_directory, f"{file_name}.html")

    # Écriture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "w") as fichier:
            fichier.write(html_page)
        # print(f"Le fichier '{chemin_fichier}' a été créé ou écrasé avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

# --------------------------------------------CSS-----------------------------------------------

    # Chemin complet du fichier
    chemin_fichier = os.path.join(script_directory, f"{file_name}.css")
    # Écriture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "w") as fichier:
            fichier.write("th, td {width: 17vw;}\n")
            fichier.write("td:hover{border:1 px solid};\n")
            fichier.write(".first_column {width:6vw;}\n")
            fichier.write(
                "table {font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n")
            fichier.write(
                ".empty {color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 1vw;}\n")
            fichier.write("#bouton-suivant {position: fixed;bottom: 2vw;right: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-suivant:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n")
            for i in range(len(liste_cours_uniques)):
                # print(liste_cours_uniques[i])
                # print(i)
                if liste_cours_uniques[i].count(' ') > 0:
                    liste_cours_uniques[i] = liste_cours_uniques[i].replace(
                        " ", "")
                # print(liste_cours_uniques[i])
                fichier.write(
                    f".{liste_cours_uniques[i]} {{background-color: {backup_color_palette[randint(0,len(backup_color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;}}\n")
        # print(f"Le fichier '{chemin_fichier}' a été créé ou écrasé avec succès.")
            fichier.write("@media (max-width: 1000px) {#bouton-suivant {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */right: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 20px;}\n")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

    # -----------------------------------------GIT--------------------------------------------------

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
        print("Les commandes Git ont été exécutées avec succès. ")
    except subprocess.CalledProcessError as e:
        print("Une erreur s'est produite lors de l'exécution des commandes Git :", e)

    return html_page


# --------------------------------------------MAIN-----------------------------------------------


# L'URL du fichier à télécharger disponible sur ADE
url = 'https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/m32jRq3k.shu'

# Envoyer une requête HTTP GET pour télécharger le fichier
response = requests.get(url)

# Récupérer la date d'aujourd'hui
acutal_date = date.today()

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Obtenir le contenu du fichier
    content = response.content

    script_directory = os.path.dirname(__file__)

    # si le fichier n'existe pas, on le crée dans le même répertoire que le script
    if not os.path.exists(os.path.join(script_directory, f"Data.ics")):
        with open(os.path.join(script_directory, f"Data.ics"), "w") as fichier:
            fichier.write("")

    # Chemin complet du fichier
    chemin_fichier = os.path.join(script_directory, f"Data.ics")

    # Écriture du contenu dans le fichier
    with open(chemin_fichier, "wb") as fichier:
        fichier.write(content)

    # print("Le fichier a été téléchargé avec succès et enregistré sous 'Data.ics'.")
else:
    print("La requête a échoué.")

# Obtenir le répertoire du script
script_directory = os.path.dirname(__file__)

# Construire le chemin relatif vers le fichier "Data.ics"
fichier_relative_path = os.path.join(script_directory, "Data.ics")

# Vérifier si le fichier existe
if os.path.exists(fichier_relative_path):
    # Ouvrir le fichier en lecture
    with open(fichier_relative_path, "rb") as f:
        cal = Calendar.from_ical(f.read())
else:
    print("Le fichier 'Data.ics' n'existe pas dans le répertoire du script.")


# Liste des couleurs pour les cours
color_palette = [
    "#F3DE8A",
    "#F4DB90",
    "#F4D796",
    "#F4D49C",
    "#F4D0A2",
    "#F4CDA8",
    "#F4C9AE",
    "#F4C5B4",
    "#F4C1B9",
    "#D7B1B2",
    "#B9A0AA",
    "#AB98A6",
    "#9C90A2",
    "#958CA0",
    "#8D889E",
    "#86849C",
    "#7E7F9A"
]

# copie de la liste de couleurs, utile pour réinitialiser la liste de couleurs
backup_color_palette = color_palette.copy()


# SEMAINE COURANTE
file_name = "index"
to_page = "index_s2"
html_and_css = generate_html_page(get_monday_date(
    date.today()), color_palette, file_name, to_page)
generate_html_file_and_css_file(
    html_and_css[0], html_and_css[1], html_and_css[2], html_and_css[3], html_and_css[4], file_name)

week_data = {}

# SEMAINE SUIVANTE
file_name = "index_s2"
to_page = "index"
html_and_css_semaine2 = generate_html_page(get_monday_date(
    date.today()) + timedelta(days=7), color_palette, file_name, to_page)
# print(get_monday_date(date.today()) + timedelta(days=7))
# print(html_and_css_semaine2[0])
generate_html_file_and_css_file(html_and_css_semaine2[0], html_and_css_semaine2[1],
                                html_and_css_semaine2[2], html_and_css_semaine2[3], html_and_css_semaine2[4], file_name)
