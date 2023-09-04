from icalendar import Calendar
import datetime
import pyperclip
from random import randint


#une liste de 50 strings de couleurs en hexadécimal dans la même gamme de couleurs
random_color_palette = ["#FFCC66", "#FFCC66", "#FFCCCC", "#FFCCFF", "#FF99CC", "#FF99FF", "#FF66CC", "#FF66FF", "#FF33CC", "#FF33FF", "#FF00CC"]

#fonction qui renvoie une liste contenant tous les event_text de la semaine
def count_events (week_data):
    all_events_text = []
    for event in week_data:
        all_events_text.append(event[2])
    return all_events_text



# Chargez le fichier .ics
with open('Timetable/September.ics', 'rb') as f:
    cal = Calendar.from_ical(f.read())

# Créez un dictionnaire pour stocker les données par jour de la semaine
week_data = {'Monday': [], 'Tuesday': [],
             'Wednesday': [], 'Thursday': [], 'Friday': []}



# Parcourez les événements du calendrier
for event in cal.walk('vevent'):
    summary = event.get('summary')
    location = event.get('location')
    start_time = event.get('dtstart').dt + datetime.timedelta(hours=2.5)  # Ajoutez 2 heures et demi car données du site mauvaises
    end_time = event.get('dtend').dt + datetime.timedelta(hours=2.5)  # Ajoutez 2 heures et demi car données du site mauvaises

    # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
    day_of_week = start_time.strftime('%A')

    # Créez une chaîne de texte pour l'événement
    event_text = f"{summary} ({location})"

    # Ajoutez l'événement au dictionnaire de données correspondant au jour de la semaine
    week_data[day_of_week].append((start_time, end_time, event_text))



#on affiche pour chaque élément de week data, le 3ème élément de la liste (event_text)



# Créez un tableau HTML
html_table = "<table border='1'>"
html_table += "<tr><th>Plage Horaire</th><th style='border: none; background-color: #FFCC66;'>Lundi</th><th style='    border: none;background-color: #FFCC99;'>Mardi</th><th style='    border: none;background-color: #FFCCCC;'>Mercredi</th><th style='    border: none;background-color: #FFCCFF;'>Jeudi</th><th style='    border: none;background-color: #FF99CC;'>Vendredi</th></tr>"

# Définissez l'heure de début (8h du matin, après avoir ajouté 2 heures)
start_hour = 8
start_minute = 0

# Définissez l'heure de fin (20h30 du soir, après avoir ajouté 2 heures)
end_hour = 20
end_minute = 30

# Parcourir les heures de 8h à 20h30 avec un intervalle de 15 minutes
current_time = datetime.datetime(
    year=2023, month=9, day=3, hour=start_hour, minute=start_minute)

#mettre les heures que une fois sur deux
one_or_two = True

liste_cours = []

# Tant que l'heure actuelle est inférieure à l'heure de fin
while current_time.hour < end_hour or (current_time.hour == end_hour and current_time.minute <= end_minute):
    html_table += "<tr>"
    
    

    # Calculer la plage horaire
    time_range_start = current_time.strftime('%H:%M')
    current_time += datetime.timedelta(minutes=15)
    time_range = f"{time_range_start}"

    # Mettre les heures sur 2 cellules, une fois sur deux
    if one_or_two : 
        color = random_color_palette[randint(0, len(random_color_palette)-1)]
        html_table += f"<td rowspan='2' style='border:none;background-color: {color}'>{time_range} ---------    </td>" 
        one_or_two = False
    else :
        one_or_two = True


    # Parcourir les jours de la semaine
    for day, events in week_data.items():
        event_texts = []
        for event_start, event_end, event_desc in events:

            if event_start.time() <= current_time.time() < event_end.time():
                event_texts.append(event_desc)

        

        # Si plusieurs événements, fusionnez-les dans une seule cellule avec rowspan
        if event_texts:
            if event_texts[0][0:5]  not in liste_cours:
                liste_cours.append(event_texts[0][0:5])
                
            else:
                rowspan = len(event_texts)
                event_text = '<br>'.join(event_texts)
                #on enleve les espces dans le nom de la classe
                n_classe = event_texts[0][0:4].replace(" ", "")
          

                html_table += f"<td  class='{n_classe}';>{event_text}</td>"
                # Ignorer les lignes fusionnées suivantes pour ce cours
                for _ in range(1, rowspan):
                    html_table += "<tr></tr>"
        else:
            html_table += "<td style='color: RGBa(128,0,128, 0);background-color: #f1f1f1;border: none;border-radius: 10px;padding: 10px;'>----------------------------------------</td>"  # Cellule vide

    html_table += "</tr>"

html_table += "</table>"

html_page = '<!DOCTYPE html><html lang="fr"><meta charset="UTF-8"><title>Emploi du temps</title><link rel="stylesheet" href="./style.css"><head>'
html_page += html_table
html_page += '</head><body></body></html>'

print(liste_cours)

#on ne garde que les 4 premiers caractères de chaque élément de liste_cours
liste_cours =  [x[0:4] for x in liste_cours]

# Imprimer ou utiliser html_table comme bon vous semble sur votre site web
# Mettre le HTML dans le presse-papiers
pyperclip.copy(html_table)

#on supprime le fichier html s'il existe déjà
import os
if os.path.exists("Timetable/index.html"):
    os.remove("Timetable/index.html")

#on crée un fichier html avec le contenu de html_page
fichier = open("Timetable/index.html", "w")
fichier.write(html_page)
fichier.close()


if os.path.exists("Timetable/style.css"):
    os.remove("Timetable/style.css")


#on crée un fichier css avec le contenu de style.css
fichier = open("Timetable/style.css", "w")
# pour chaque élément de liste_cours, on crée une classe css avec une couleur dans la liste random_color_palette
print(len(liste_cours))
for i in range(len(liste_cours)):
    if liste_cours[i].count(' ') > 0:
        liste_cours[i] = liste_cours[i].replace(" ", "")
    fichier.write(f".{liste_cours[i]} {{background-color: {random_color_palette[i]}; border: none;border-radius: 10px;padding: 10px;}}\n")
fichier.close()



