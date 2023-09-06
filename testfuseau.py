import pytz
from datetime import datetime

def convertir_heure_gmt_vers_locale(heure_gmt, pays):
    try:
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

# Exemple d'utilisation
heure_gmt = '2023-09-03 12:00:00'  # Heure GMT
pays = 'Europe/Paris'  # Pays (Fuseau horaire de Paris)

heure_locale = convertir_heure_gmt_vers_locale(heure_gmt, pays)
print(f"Heure locale en {pays}: {heure_locale.strftime('%Y-%m-%d %H:%M:%S')}")
