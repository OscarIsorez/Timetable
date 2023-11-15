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

"""
    fonction qui prend en param?tre l'heure GMT et le pays et qui renvoie l'heure locale du pays
"""


def convertir_heure_gmt_vers_locale(heure_gmt, pays):
    try:
        heure_gmt = str(heure_gmt)[0:-6]

        # Obtenez le fuseau horaire du pays spécifié

        fuseau_pays = pytz.timezone(pays)

        # Créez un objet datetime avec l'heure GMT

        heure_gmt = datetime.strptime(heure_gmt, "%Y-%m-%d %H:%M:%S")

        heure_gmt = pytz.utc.localize(heure_gmt)

        # Convertissez l'heure GMT en heure locale du pays

        heure_locale = heure_gmt.astimezone(fuseau_pays)

        return heure_locale

    except Exception as e:
        return f"Erreur : {str(e)}"


""" 
    fonction qui prend en param?tre la liste des événements de la semaine et
    qui renvoie la liste des textes des événements de la semaine
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
    # on récup?re le jour de la semaine de la date d'aujourd'hui
    day = date.weekday()

    # si le jour est lundi, on renvoie la date d'aujourd'hui
    if day == 0:
        return date

    # si le jour est samedi ou dimanche, on renvoit la date du lundi suivant
    elif day == 5:
        return date + timedelta(days=2)
    elif day == 6:
        return date + timedelta(days=1)

    # sinon on renvoie la date d'aujourd'hui moins le nombre de jours qui sépare la date d'aujourd'hui du lundi de la semaine
    else:
        return date - timedelta(days=day)


"""

    @param un objet date de la classe datetime
    @return true si le jour est un vendredi et false sinon

"""


def is_friday(date) -> bool:
    return date.weekday() == 4


"""
    fonction qui initialise le dictionnaire week_data avec les événements de la semaine
    Exemple : week_data = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
"""


def treat_data(date_to_treat):
    # Créez un dictionnaire pour stocker les données par jour de la semaine
    week_data = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }

    # Parcourez les événements du calendrier

    for event in cal.walk("vevent"):
        # si la date dstat est comprise entre date_to_treat et date_to_treat + 4 jours
        if event.get("dtstart").dt.date() >= date_to_treat and event.get(
            "dtstart"
        ).dt.date() <= date_to_treat + timedelta(days=4):
            # Obtenez les informations de l'événement
            summary = event.get("summary")

            location = event.get("location")

            start_time = convertir_heure_gmt_vers_locale(
                event.get("dtstart").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)

            end_time = convertir_heure_gmt_vers_locale(
                event.get("dtend").dt, "Europe/Paris"
            ) + timedelta(hours=0.5)

            # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
            day_of_week = start_time.strftime("%A")

            # Créez une chaine de texte pour l'événement
            event_texts = f"{summary} ({location})"

            # Ajoutez l'événement au dictionnaire de données correspondant au jour de la semaine
            week_data[day_of_week].append((start_time, end_time, event_texts))

            # on affiche tous les event_texts dans la console

    return week_data

    # ----------------------------------GESTION DU CODE HTML-------------------------------------------------------------------------------------------


"""
    fonction qui prend en param?tre la date du lundi de la semaine a  traiter, la liste des couleurs pour les cours et le nom du fichier html a  créer
    et qui renvoie le code html de la page
"""


def generate_html_data(
    date_to_treat, color_palette, file_name, to_page, from_page=None
):
    global button_text

    week_data = treat_data(date_to_treat)

    # Créez un tableau HTML
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
    html_table += f"<tr><th class='top_left'>Semaine du {top_left}</th><th style='border: none; background-color:{color_palette[0]};'>Lundi</th><th style='border: none;background-color: {color_palette[1]};'>Mardi</th><th style='border: none;background-color: {color_palette[2]};'>Mercredi</th><th style='border: none;background-color: {color_palette[3]};'>Jeudi</th><th  style='border: none;background-color: {color_palette[4]};'>Vendredi</th></tr>"

    # Définissez l'heure de début (8h du matin, apr?s avoir ajouté 2 heures)
    start_hour = 8
    start_minute = 0

    # Définissez l'heure de fin (20h30 du soir, apr?s avoir ajouté 2 heures)
    end_hour = 19
    end_minute = 0

    # on utilisera la biblioth?que datetime pour créer un objet datetime
    current_time = datetime(
        year=acutal_date.year,
        month=acutal_date.month,
        day=acutal_date.day,
        hour=start_hour,
        minute=start_minute,
    )

    # mettre les heures que une fois sur deux
    one_or_two = True

    # liste qui contiendra les cours de la semaine, avec les heures de début et de fin
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

    # on change le texte du bouton pour la page suivante ? la page pr?c?dente
    button_text = "Page preceedente"
    return html_page, liste_cours, liste_cours_uniques, color_palette


# ----------------------------GESTION DES FICHIERS-------------------------------------------------------------------------------------------
"""
    fonction qui crée le fichier html et le fichier css si nécessaire ou 
    écrase les fichiers existants pour les mettre a jour
"""


def generate_html_file_and_css_file(
    html_page, liste_cours, liste_cours_uniques, color_palette, file_name
):
    # liste_cours contient des tableaux de 2 éléments. on souhaite garder uniquement les 4 premiers caract?res de l'élément 0
    for i in range(len(liste_cours)):
        if "CC" in liste_cours[i][0]:
            liste_cours[i][0] = liste_cours[i][0][0:4] + "-Controle-Continu"
        elif "-last_column" in liste_cours[i][0][0]:
            liste_cours[i][0] = liste_cours[i][0][0:4] + "-last_column"
        else:
            liste_cours[i][0] = liste_cours[i][0][0:4]

    # la liste contenant elle meme des listes, on ne gardera que le premier élément de chaque élément
    liste_cours_uniques = []

    for i in range(len(liste_cours)):
        liste_cours_uniques.append(liste_cours[i][0])

    # on supprime les doublons
    liste_cours_uniques = list(set(liste_cours_uniques))

    # --------------------------------------------HTML----------------------------------------------------------------------------------------------

    # Obtenir le répertoire du script
    script_directory = os.path.dirname(__file__)

    # Chemin complet du fichier "index.html"
    chemin_fichier = os.path.join(script_directory, f"{file_name}.html")

    # écriture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "w", encoding="iso-8859-2") as fichier:
            fichier.write(html_page)

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ecriture dans le fichier: {str(e)}")

    # --------------------------------------------CSS----------------------------------------------------------------------------------------------

    # Chemin complet du fichier
    chemin_fichier = os.path.join(
        script_directory,
        f"style.css",  # a modifier plus tard pour n'avoir qu'un CSS commun /{file_name[-2] + file_name[-1]}
    )

    # écriture du contenu HTML dans le fichier
    try:
        with open(chemin_fichier, "a", encoding="iso-8859-2") as fichier:
            fichier.write(
                "th, td {width: 17vw; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n"
            )
            fichier.write(
                "* {font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;}\n"
            )
            fichier.write(
                ".empty {color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 1vw;height: 20px;}\n"
            )
            fichier.write(
                "#bouton-suivant {position: fixed;bottom: 2vw;right: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-suivant:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
            fichier.write(
                "#bouton-precedent {position: fixed;bottom: 2vw;left: 2vw;background-color: #ffffff;color: #8D889EB9;padding: 1vw 2vw;border: 2px solid #8D889EB9;border-radius: 5px;cursor: pointer; text-align: center;text-decoration: none;display: inline-block;font-size: 1vw;border-radius: 7px;transition: background-color 0.3s, border-color 0.3s, color 0.3s;}#bouton-precedent:hover {background-color: #8D889EB9;border-color: #8D889EB9;    color: #ffffff;}\n"
            )
            for i in range(len(liste_cours_uniques)):
                if liste_cours_uniques[i].count(" ") > 0:
                    liste_cours_uniques[i] = liste_cours_uniques[i].replace(" ", "")
                if "-Controle-Continu" in liste_cours_uniques[i]:
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: #B81717; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;}}\n"
                    )
                elif "-last_column" in liste_cours_uniques[i]:
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: {color_palette[randint(0,len(color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 1.05;transition: 0.5s}}\n"
                    )
                    fichier.write(
                        f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 1.2;    translate: -8vw;}}\n"
                    )
                else:
                    print(liste_cours_uniques[i])
                    fichier.write(
                        f".{liste_cours_uniques[i]} {{background-color: {color_palette[randint(0,len(color_palette) -1)]}; border: none;border-radius: 10px;padding: 1vw;text-align: center; user-select:none;}}\n"
                    )
                    # le contenu du fichuer
                    print(
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

            fichier.write(
                "@media (max-width: 1000px) {#bouton-suivant {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */right: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}#bouton-precedent {padding: 4vw 5vw;/* Augmenter le padding */bottom: 4vw;/* Augmenter la distance depuis le bas */left: 4vw;/* Augmenter la distance depuis la droite *//*on arrondie les angles*/border-radius: 30px;font-size: 3vw;}\n"
            )
            for i in range(len(liste_cours_uniques)):
                fichier.write(
                    f".{liste_cours_uniques[i]}:hover {{ border: 1px solid;scale: 2;transition: 0.5s}}\n"
                )
                fichier.write(
                    f".{liste_cours_uniques[i]}:active {{border: 1px solid;scale: 2.2;}}\n"
                )
            fichier.write("}\n")

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'ecriture du fichier CSS: {str(e)}")


# -----------------------------------------GIT---------------------------------------------------------------------------------------


def git_commands():
    repo_directory = "C:/Users/Oscar/OneDrive/Documents/Timetable/Timetable"

    git_add_command = ["git", "add", "."]

    git_commit_command = ["git", "commit", "-m", "update"]

    git_push_command = ["git", "push"]

    try:
        subprocess.run(git_add_command, cwd=repo_directory, check=True)
        subprocess.run(git_commit_command, cwd=repo_directory, check=True)
        subprocess.run(git_push_command, cwd=repo_directory, check=True)
        print("Les commandes Git ont été exécutées avec succ?s. ")
        print("")

    except subprocess.CalledProcessError as e:
        print("Une erreur s'est produite lors de l'exécution des commandes Git :", e)


# --------------------------------------------MAIN---------------------------------------------------------------------------------------------

button_text = "Semaine suivante"
button_text.encode("iso-8859-2")


url = "https://planning.univ-rennes1.fr/jsp/custom/modules/plannings/o35ex53R.shu"


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
    # print("Le fichier a été téléchargé avec succ?s et enregistré sous 'Data.ics'.")

else:
    print("La requete a échoué.")


script_directory = os.path.dirname(__file__)


fichier_relative_path = os.path.join(script_directory, "Data.ics")

if os.path.exists(fichier_relative_path):
    with open(fichier_relative_path, "r", encoding="iso-8859-2") as f:
        cal = Calendar.from_ical(f.read())

else:
    print("Le fichier 'Data.ics' n'existe pas dans le répertoire du script.")


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
]

backup_color_palette = color_palette.copy()

"""
fonction qui prend en entrée un n, nombre de semaine ? afficher et qui gén?re les pages et le code html associé
"""


def generate_weeks(n):
    if n <= 0:
        print("Le nombre de semaines doit etre positif")
        return
    if n == 1:
        generate_first_week(to_page="None")
    else:
        generate_first_week()
        generate_mid_weeks(n)
        generate_last_week(n)


def generate_first_week(to_page="index_s2"):
    file_name = "index"

    html_and_css = generate_html_data(
        get_monday_date(date.today()), color_palette, file_name, to_page
    )

    generate_html_file_and_css_file(
        html_and_css[0], html_and_css[1], html_and_css[2], html_and_css[3], file_name
    )


"""
@param : n, nombre de semaines ? afficher, qui sera utile car égal au numéro de la derni?re page ? créer
"""


def generate_last_week(n):
    file_name = f"index_s{n}"
    to_page = "None"
    from_page = f"index_s{n-1}"

    html_and_css_semaine = generate_html_data(
        get_monday_date(date.today()) + timedelta(days=7 * n),
        color_palette,
        file_name,
        to_page,
        from_page=from_page,
    )

    generate_html_file_and_css_file(
        html_and_css_semaine[0],
        html_and_css_semaine[1],
        html_and_css_semaine[2],
        html_and_css_semaine[3],
        file_name,
    )


def generate_mid_weeks(n):
    for i in range(2, n):
        file_name = f"index_s{i}"
        to_page = f"index_s{i+1}"
        from_page = f"index_s{i-1}"
        if i == 2:
            from_page = "index"

        html_and_css_semaine = generate_html_data(
            get_monday_date(date.today()) + timedelta(days=7 * (i - 1)),
            color_palette,
            file_name,
            to_page,
            from_page=from_page,
        )

        generate_html_file_and_css_file(
            html_and_css_semaine[0],
            html_and_css_semaine[1],
            html_and_css_semaine[2],
            html_and_css_semaine[3],
            file_name,
        )


def supprimer_lignes_en_doublon(chemin_fichier_entree, chemin_fichier_sortie):
    try:
        # Ouverture du fichier d'entrée en mode lecture
        with open(chemin_fichier_entree, "r") as fichier_entree:
            # Lecture des lignes du fichier d'entrée et suppression des doublons
            lignes_uniques = set(fichier_entree.readlines())

        # Ouverture du fichier de sortie en mode écriture
        with open(chemin_fichier_sortie, "w") as fichier_sortie:
            # Écriture des lignes uniques dans le fichier de sortie
            fichier_sortie.writelines(lignes_uniques)

        print(
            f"Les lignes en doublon ont été supprimées. Le fichier modifié est disponible ? l'emplacement : {chemin_fichier_sortie}"
        )

    except FileNotFoundError:
        print(f"Le fichier {chemin_fichier_entree} n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# Exemple d'utilisation :
# Supprimer les lignes en doublon du fichier 'exemple.txt' et enregistrer le résultat dans 'exemple_modifie.txt'


git_commands()
generate_weeks(10)
supprimer_lignes_en_doublon("style.css", "style_m.css")
