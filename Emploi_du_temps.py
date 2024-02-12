# -*- coding: iso-8859-2 -*-


from icalendar import Calendar

from datetime import date, timedelta, datetime

import pyperclip
from random import randint

import requests
import os

import subprocess

import pytz

import sys

sys.stdout.reconfigure(encoding="iso-8859-2")
sys.stdout.reconfigure(encoding="iso-8859-2")

"""
    fonction qui prend en param?tre l'heure GMT et le pays et qui renvoie l'heure locale du pays
"""


def convertir_heure_gmt_vers_locale(heure_gmt, pays):
    try:
        heure_gmt = str(heure_gmt)[0:-6]

        # Obtenez le fuseau horaire du pays sp�cifi�

        fuseau_pays = pytz.timezone(pays)

        # Cr�ez un objet datetime avec l'heure GMT

        heure_gmt = datetime.strptime(heure_gmt, "%Y-%m-%d %H:%M:%S")
        heure_gmt = datetime.strptime(heure_gmt, "%Y-%m-%d %H:%M:%S")

        heure_gmt = pytz.utc.localize(heure_gmt)

        # Convertissez l'heure GMT en heure locale du pays

        heure_locale = heure_gmt.astimezone(fuseau_pays)

        return heure_locale

    except Exception as e:
        return f"Erreur : {str(e)}"


""" 
    fonction qui prend en param?tre la liste des �v�nements de la semaine et
    qui renvoie la liste des textes des �v�nements de la semaine
"""


def count_events(week_data):
    all_events_text = []

    for event in week_data:
        all_events_text.append(event[2])

    return all_events_text


""" 
    fonction qui prend en param?tre la date d'aujourd'hui et
    qui renvoie la date du lundi de la semaine dans laquelle se trouve la date d'aujourd'hui
"""


def get_monday_date(date):
    # on r�cup?re le jour de la semaine de la date d'aujourd'hui
    day = date.weekday()

    # si le jour est lundi, on renvoie la date d'aujourd'hui
    if day == 0:
        return date

    # si le jour est samedi ou dimanche, on renvoit la date du lundi suivant
    elif day == 5:
        return date + timedelta(days=2)
    elif day == 6:
        return date + timedelta(days=1)

    # sinon on renvoie la date d'aujourd'hui moins le nombre de jours qui s�pare la date d'aujourd'hui du lundi de la semaine
    else:
        return date - timedelta(days=day)


"""

    @param un objet date de la classe datetime
    @return true si le jour est un vendredi et false sinon

"""




def is_friday(date) -> bool:
    return date.weekday() == 4


"""
    fonction qui initialise le dictionnaire week_data avec les �v�nements de la semaine
    Exemple : week_data = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
"""


def treat_data(date_to_treat):
    # Cr�ez un dictionnaire pour stocker les donn�es par jour de la semaine
    week_data = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }
    week_data = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }

    # Parcourez les �v�nements du calendrier

    for event in cal.walk("vevent"):

        # si la date dstat est comprise entre date_to_treat et date_to_treat + 4 jours
        if event.get("dtstart").dt.date() >= date_to_treat and event.get(
            "dtstart"
        ).dt.date() <= date_to_treat + timedelta(days=4):
        if event.get("dtstart").dt.date() >= date_to_treat and event.get(
            "dtstart"
        ).dt.date() <= date_to_treat + timedelta(days=4):
            # Obtenez les informations de l'�v�nement
            summary = event.get("summary")
            summary = event.get("summary")

            location = event.get("location")
            location = event.get("location")

            start_time = convertir_heure_gmt_vers_locale(
                event.get("dtstart").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)
                event.get("dtstart").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)

            end_time = convertir_heure_gmt_vers_locale(
                event.get("dtend").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)
                event.get("dtend").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)

            # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
            day_of_week = start_time.strftime("%A")
            day_of_week = start_time.strftime("%A")

            # Cr�ez une chaine de texte pour l'�v�nement
            event_texts = f"{summary} ({location})"

            # Ajoutez l'�v�nement au dictionnaire de donn�es correspondant au jour de la semaine
            week_data[day_of_week].append((start_time, end_time, event_texts))

            # on affiche tous les event_texts dans la console

    return week_data

    # ----------------------------------GESTION DU CODE HTML-------------------------------------------------------------------------------------------


"""
    fonction qui prend en param?tre la date du lundi de la semaine a� traiter, la liste des couleurs pour les cours et le nom du fichier html a� cr�er
    et qui renvoie le code html de la page
"""


def generate_html_data(
    date_to_treat, color_palette, file_name, to_page, from_page=None
):
def generate_html_data(
    date_to_treat, color_palette, file_name, to_page, from_page=None
):
    global button_text

    week_data = treat_data(date_to_treat)

    # Cr�ez un tableau HTML
    html_table = ""
    html_table += "<table border='1'>"
    top_left = (
        str(date_to_treat.day)
        + " \nau "
        + str((date_to_treat + timedelta(days=4)).day)
        + "<br>"
        + str((date_to_treat + timedelta(days=4)).month)
        + "-"
        + str((date_to_treat + timedelta(days=4)).year)
    )
    top_left = (
        str(date_to_treat.day)
        + " \nau "
        + str((date_to_treat + timedelta(days=4)).day)
        + "<br>"
        + str((date_to_treat + timedelta(days=4)).month)
        + "-"
        + str((date_to_treat + timedelta(days=4)).year)
    )
    html_table += f"<tr><th class='top_left'>Semaine du {top_left}</th><th style='border: none; background-color:{color_palette[0]};'>Lundi</th><th style='border: none;background-color: {color_palette[1]};'>Mardi</th><th style='border: none;background-color: {color_palette[2]};'>Mercredi</th><th style='border: none;background-color: {color_palette[3]};'>Jeudi</th><th  style='border: none;background-color: {color_palette[4]};'>Vendredi</th></tr>"

    # D�finissez l'heure de d�but (8h du matin, apr?s avoir ajout� 2 heures)
    start_hour = 8
    start_minute = 0

    # D�finissez l'heure de fin (20h30 du soir, apr?s avoir ajout� 2 heures)
    end_hour = 19
    end_minute = 0

    # on utilisera la biblioth?que datetime pour cr�er un objet datetime
    current_time = datetime(
        year=acutal_date.year,
        month=acutal_date.month,
        day=acutal_date.day,
        hour=start_hour,
        minute=start_minute,
    )
        year=acutal_date.year,
        month=acutal_date.month,
        day=acutal_date.day,
        hour=start_hour,
        minute=start_minute,
    )

    # mettre les heures que une fois sur deux
    one_or_two = True

    # liste qui contiendra les cours de la semaine, avec les heures de d�but et de fin
    liste_cours = []
    liste_cours_vendredi = []
    # liste qui contiendra les cours de la semaine sans les doublons
    liste_cours_uniques = []

    while current_time.hour < end_hour or (
        current_time.hour == end_hour and current_time.minute <= end_minute
    ):

        html_table += "<tr>"

        # Calculer la plage horair
        time_range_start = current_time.strftime("%H:%M")
        time_range_start = current_time.strftime("%H:%M")
        current_time += timedelta(minutes=15)
        time_range = f"{time_range_start}"

        # Mettre les heures sur 2 cellules, une fois sur deux
        if one_or_two:
            color = color_palette[0]
            color_palette.pop(0)
            color_palette.append(color)
            html_table += f"<td rowspan='2' style='border:none;background-color: {color}' class='first_column' > {str(time_range)}</td>"
            one_or_two = False

        else:
            one_or_two = True

        # Parcourir les jours de la semaine

        for day, events in week_data.items():
            event_informations = []

            for event_start, event_end, event_desc in events:
                if event_start.time() <= current_time.time() < event_end.time():
                    event_informations.append([event_desc, event_start, event_end])
                    event_informations.append([event_desc, event_start, event_end])

            if event_informations:
                if day == "Friday":
                    liste_cours_vendredi.append(event_informations[0])

                if event_informations[0] not in liste_cours:
                    n_classe = event_informations[0][0][0:4].replace(" ", "")
                    # if day == "Friday":
                    #     n_classe += "-last_column"
                    #     # event_informations[0] = [str(event_informations[0][0]) + '-last_column', event_informations[0][1], event_informations[0][2]]
                    #     liste_cours.append(event_informations[0])
                    # else :
                    liste_cours.append(event_informations[0])
                    event_desc = str(event_informations[0][0])
                    # on enleve les espces dans le nom de la classe
                    if "CC" in event_desc:
                        n_classe += "-Controle-Continu"
                    nbr_rowspan = (
                        event_informations[0][2] - event_informations[0][1]
                    ) // timedelta(minutes=15)
                        event_informations[0][2] - event_informations[0][1]
                    ) // timedelta(minutes=15)
                    html_table += f"<td  rowspan='{nbr_rowspan} 'class='{n_classe}';>{event_desc}</td>"
            else:
                # Cellule vide
                html_table += "<td class='empty'></td>"

        html_table += "</tr>"

    html_table += "</table>"

    # date actuelle, en arrondissant les secondes ? l'entier pret
    actual_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    html_page = f'<!DOCTYPE html><html lang="fr"><head><meta charset="iso-8859-2"><title>Emploi du temps</title><link rel="stylesheet" href="./style.css"><link rel="icon" href="./favicon.ico" type="image/x-icon" sizes="32x32"></head><body><p class="date"> Mise a jour : {actual_date}</p>   '
    html_page += html_table
    if to_page != "None":
        html_page += f'<button id="bouton-suivant" onclick="window.location.href=\'./{to_page}.html\'">Page suivante</button>'
    if from_page:
        html_page += f'<button id="bouton-precedent" onclick="window.location.href=\'./{from_page}.html\'">Page precedente</button>'
    html_page += "</body></html>"
    html_page += "</body></html>"

    # on change le texte du bouton pour la page suivante ? la page pr?c?dente
    button_text = "Page preceedente"
    return html_page, liste_cours, liste_cours_uniques, color_palette


# ----------------------------GESTION DES FICHIERS-------------------------------------------------------------------------------------------
"""
    fonction qui cr�e le fichier html et le fichier css si n�cessaire ou 
    �crase les fichiers existants pour les mettre a jour
"""


def generate_html_file_and_css_file(
    html_page, liste_cours, liste_cours_uniques, color_palette, file_name
):
def generate_html_file_and_css_file(
    html_page, liste_cours, liste_cours_uniques, color_palette, file_name
):
    # liste_cours contient des tableaux de 2 �l�ments. on souhaite garder uniquement les 4 premiers caract?res de l'�l�ment 0
    for i in range(len(liste_cours)):
        if "CC" in liste_cours[i][0]:
            liste_cours[i][0] = liste_cours[i][0][0:4] + "-Controle-Continu"
        elif "-last_column" in liste_cours[i][0][0]:
            liste_cours[i][0] = liste_cours[i][0][0:4] + "-last_column"
        else:
            liste_cours[i][0] = liste_cours[i][0][0:4]

    # la liste contenant elle meme des listes, on ne gardera que le premier �l�ment de chaque �l�ment
    liste_cours_uniques = []

    for i in range(len(liste_cours)):
        liste_cours_uniques.append(liste_cours[i][0])

    # on supprime les doublons
    liste_cours_uniques = list(set(liste_cours_uniques))

    # --------------------------------------------HTML----------------------------------------------------------------------------------------------

    # Obtenir le r�pertoire du script
    script_directory = os.path.dirname(__file__)

    # Chemin complet du fichier "index.html"
    chemin_fichier = os.path.join(script_directory, f"{file_name}.html")

    # �criture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "w", encoding="iso-8859-2") as fichier:
            fichier.write(html_page)

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ecriture dans le fichier: {str(e)}")
        print(f"Une erreur s'est produite lors de l'ecriture dans le fichier: {str(e)}")

    # --------------------------------------------CSS----------------------------------------------------------------------------------------------

    # Chemin complet du fichier
    chemin_fichier = os.path.join(
        script_directory, f"style-{file_name[-2] + file_name[-1]}.css"
    )

    # �criture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "a", encoding="iso-8859-2") as fichier:
            fichier.write(
                "th, td {width: 17vw; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n"
            )
            fichier.write(
                "th, td {width: 17vw; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n"
            )
            fichier.write(
                "* {font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n"
            )
            fichier.write(
                ".empty {color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 1vw;height: 20px;}\n"
            )
                ".empty {color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 1vw;height: 20px;}\n"
            )
            fichier.write(
                "#bouton-suivant {position: fixed;bottom: 2vw;right: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-suivant:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
                "#bouton-suivant {position: fixed;bottom: 2vw;right: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-suivant:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
            fichier.write(
                "#bouton-precedent {position: fixed;bottom: 2vw;left: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-precedent:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
                "#bouton-precedent {position: fixed;bottom: 2vw;left: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-precedent:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
            for i in range(len(liste_cours_uniques)):
                # print(liste_cours_uniques[i])
                # print(i)
                if liste_cours_uniques[i].count(" ") > 0:
                    liste_cours_uniques[i] = liste_cours_uniques[i].replace(" ", "")
                if "-Controle-Continu" in liste_cours_uniques[i]:
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: #B81717; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                        f".{liste_cours_uniques[i]} {{background-color: #B81717; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;}}\n"
                    )
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;}}\n"
                    )
                elif "-last_column" in liste_cours_uniques[i]:
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: {color_palette[randint(0,len(color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                        f".{liste_cours_uniques[i]} {{background-color: {color_palette[randint(0,len(color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;    translate: -8vw;}}\n"
                    )
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;    translate: -8vw;}}\n"
                    )
                else:
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: {color_palette[randint(0,len(color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;}}\n"
                    )
            fichier.write(".first_column {width:15vw;text-align: right;height: 8vw;}\n")
            fichier.write(".top_left {width:15vw;text-align: center;}\n")

            # print(f"Le fichier '{chemin_fichier}' a �t� cr�� ou �cras� avec succ?s.")

            fichier.write(
                "@media (max-width: 1000px) {#bouton-suivant {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */right: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}#bouton-precedent {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */left: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}\n"
            )
                "@media (max-width: 1000px) {#bouton-suivant {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */right: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}#bouton-precedent {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */left: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}\n"
            )
            for i in range(len(liste_cours_uniques)):
                fichier.write(
                    f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 2;transition: 0.5s}}\n"
                )
                    f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 2;transition: 0.5s}}\n"
                )
                fichier.write(
                    f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 2.2;}}\n"
                )
            fichier.write("}\n")
                    f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 2.2;}}\n"
                )
            fichier.write("}\n")

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ecriture du fichier CSS: {str(e)}")
        print(f"Une erreur s'est produite lors de l'ecriture du fichier CSS: {str(e)}")


# -----------------------------------------GIT---------------------------------------------------------------------------------------



def git_commands():

    # Sp�cifiez le r�pertoire dans lequel vous souhaitez ex�cuter les commandes Git
    repo_directory = "C:/Users/Oscar/OneDrive/Documents/Timetable/Timetable"

    # Commande Git : git add .
    git_add_command = ["git", "add", "."]

    # Commande Git : git commit -m "update"
    git_commit_command = ["git", "commit", "-m", "update"]

    # Commande Git : git push
    git_push_command = ["git", "push"]

    # Ex�cutez les commandes Git dans le r�pertoire du d�pat

    try:
        subprocess.run(git_add_command, cwd=repo_directory, check=True)
        subprocess.run(git_commit_command, cwd=repo_directory, check=True)
        subprocess.run(git_push_command, cwd=repo_directory, check=True)
        print("Les commandes Git ont �t� ex�cut�es avec succ?s. ")
        print("")

    except subprocess.CalledProcessError as e:
        print("Une erreur s'est produite lors de l'ex�cution des commandes Git :", e)


# --------------------------------------------MAIN---------------------------------------------------------------------------------------------

button_text = "Semaine suivante"
button_text.encode("iso-8859-2")


# L'URL du fichier a� t�l�charger disponible sur ADE
url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/6YP8G1Yv.shu"


response = requests.get(url)

acutal_date = date.today()

if response.status_code == 200:
    content = response.content

    script_directory = os.path.dirname(__file__)

    if not os.path.exists(os.path.join(script_directory, f"Data.ics")):
        with open(os.path.join(script_directory, f"Data.ics"), "w") as fichier:
            fichier.write("")

    chemin_fichier = os.path.join(script_directory, f"Data.ics")

    with open(chemin_fichier, "wb") as fichier:
        fichier.write(content)
    # print("Le fichier a �t� t�l�charg� avec succ?s et enregistr� sous 'Data.ics'.")

else:
    print("La requete a �chou�.")


script_directory = os.path.dirname(__file__)


fichier_relative_path = os.path.join(script_directory, "Data.ics")

if os.path.exists(fichier_relative_path):
    with open(fichier_relative_path, "r", encoding="iso-8859-2") as f:
        cal = Calendar.from_ical(f.read())

else:
    print("Le fichier 'Data.ics' n'existe pas dans le r�pertoire du script.")


color_palette = [
    "#F3DE8A",
    "#F4DB90",
    "#F4D796",
    "#F4D49C",
    "#F4D29F",
    "#F4D0A2",
    "#F4CFA5",
    "#F4CDA8",
    "#F4CBAB",
    "#F4CAAD",
    "#F4C9AE",
    "#F4C5B4",
    "#F4C3B7",
    "#F4C1B9",
    "#E6B9B6",
    "#DFB5B4",
    "#DBB3B3",
    "#D7B1B2",
    "#B9A0AA",
    "#AB98A6",
    "#9C90A2",
    "#958CA0",
    "#8D889E",
    "#86849C",
    "#7E7F9A",
    "#7E7F9A",
]

backup_color_palette = color_palette.copy()

# SEMAINE COURANTE

file_name = "index"  # le nom du fichier html et css
# le nom de la page vers laquelle on ira en cliquant sur le bouton du site
to_page = "index_s2"

html_and_css = generate_html_data(
    get_monday_date(date.today()), color_palette, file_name, to_page
)

generate_html_file_and_css_file(
    html_and_css[0], html_and_css[1], html_and_css[2], html_and_css[3], file_name
)


# on r�initialise la liste des couleurs pour les cours et le dictionnaire week_data de donn�es de la semaine courante
week_data = {}
color_palette = backup_color_palette.copy()


# SEMAINE SUIVANTE

file_name = "index_s2"  # le nom du fichier html et css
to_page = "index_s3"
from_page = "index"

html_and_css_semaine2 = generate_html_data(
    get_monday_date(date.today()) + timedelta(days=7),
    color_palette,
    file_name,
    to_page,
    from_page=from_page,
)

generate_html_file_and_css_file(
    html_and_css_semaine2[0],
    html_and_css_semaine2[1],
    html_and_css_semaine2[2],
    html_and_css_semaine2[3],
    file_name,
)


week_data = {}
color_palette = backup_color_palette.copy()

# SEMINE SUIVANTE

file_name = "index_s3"  # le nom du fichier html et css
to_page = "index_s4"  # s'il n'y a pas de page suivante, mettre to_page = "None"
from_page = "index_s2"

html_and_css_semaine3 = generate_html_data(
    get_monday_date(date.today()) + timedelta(days=14),
    color_palette,
    file_name,
    to_page,
    from_page=from_page,
)

generate_html_file_and_css_file(
    html_and_css_semaine3[0],
    html_and_css_semaine3[1],
    html_and_css_semaine3[2],
    html_and_css_semaine3[3],
    file_name,
)


week_data = {}
color_palette = backup_color_palette.copy()

# SEMAINE SUIVANTE

file_name = "index_s4"  # le nom du fichier html et css
to_page = "index_s5"  # s'il n'y a pas de page suivante, mettre to_page = "None"
from_page = "index_s3"

html_and_css_semaine4 = generate_html_data(
    get_monday_date(date.today()) + timedelta(days=21),
    color_palette,
    file_name,
    to_page,
    from_page=from_page,
)

generate_html_file_and_css_file(
    html_and_css_semaine4[0],
    html_and_css_semaine4[1],
    html_and_css_semaine4[2],
    html_and_css_semaine4[3],
    file_name,
)

week_data = {}
color_palette = backup_color_palette.copy()


# SEMAINE SUIVANTE

file_name = "index_s5"  # le nom du fichier html et css
to_page = "None"  # s'il n'y a pas de page suivante, mettre to_page = "None"
from_page = "index_s4"

html_and_css_semaine5 = generate_html_data(
    get_monday_date(date.today()) + timedelta(days=28),
    color_palette,
    file_name,
    to_page,
    from_page=from_page,
)

generate_html_file_and_css_file(
    html_and_css_semaine5[0],
    html_and_css_semaine5[1],
    html_and_css_semaine5[2],
    html_and_css_semaine5[3],
    file_name,
)


""" 
    fonction qui prend en param?tre un entier n, nombre de semaines et g�n?re n pages affichant l'emploi du temps, semaine par semaine
"""


def main(n):

    week_data = {}
    color_palette = backup_color_palette.copy()
    n_fichier_courant = 2
    n_fichier_precedent = 1
    n_fichier_suivant = 3


print(is_friday(date.today()))

# on ex�cute les commandes git pour mettre a� jour le repository
git_commands()
generate_weeks(10)
# supprimer_lignes_en_doublon("style.css")
