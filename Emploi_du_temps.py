from icalendar import Calendar
import datetime
import pyperclip

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
    start_time = event.get('dtstart').dt + datetime.timedelta(hours=2.5)  # Ajoutez 2 heures
    end_time = event.get('dtend').dt + datetime.timedelta(hours=2.5)  # Ajoutez 2 heures

    # Obtenez le nom du jour de la semaine (Lundi, Mardi, etc.)
    day_of_week = start_time.strftime('%A')

    # Créez une chaîne de texte pour l'événement
    event_text = f"{summary} ({location})"

    # Ajoutez l'événement au dictionnaire de données correspondant au jour de la semaine
    week_data[day_of_week].append((start_time, end_time, event_text))

# Créez un tableau HTML
html_table = "<table border='1'>"
html_table += "<tr><th>Plage Horaire</th><th>Lundi</th><th>Mardi</th><th>Mercredi</th><th>Jeudi</th><th>Vendredi</th></tr>"

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

while current_time.hour < end_hour or (current_time.hour == end_hour and current_time.minute <= end_minute):
    html_table += "<tr>"
    

    # Calculer la plage horaire
    time_range_start = current_time.strftime('%H:%M')
    current_time += datetime.timedelta(minutes=15)
    time_range = f"{time_range_start}"

    # Mettre les heures sur 2 cellules, une fois sur deux
    if one_or_two : 
        html_table += f"<td rowspan='2'>{time_range}</td>" 
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
            rowspan = len(event_texts)
            event_text = '<br>'.join(event_texts)
            html_table += f"<td rowspan='{rowspan}'>{event_text}</td>"
            # Ignorer les lignes fusionnées suivantes pour ce cours
            for _ in range(1, rowspan):
                html_table += "<tr></tr>"
        else:
            html_table += "<td> ---------------------------------------- </td>"  # Cellule vide

    html_table += "</tr>"

html_table += "</table>"

# Imprimer ou utiliser html_table comme bon vous semble sur votre site web
# Mettre le HTML dans le presse-papiers
pyperclip.copy(html_table)
