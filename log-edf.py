# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:59:32 2024

@author: Nicolas
"""

import requests
from bs4 import BeautifulSoup
import time

# Fonction pour récupérer les données d'une station donnée
def scrape_station(url):
    # Faire la requête GET vers l'URL
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Parser le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Récupérer les données de toutes les stations
        stations_data = []
        sondes = soup.find_all(class_='sonde-infowindow')
        for sonde in sondes:
            data = {}
            data['sonde'] = sonde.find('h3').text.strip()
            # Extraire la date et l'heure du dernier relevé
            date_heure = sonde.find(class_='date').text.strip().split(" : ")[1]
            # Remplacer les retours à la ligne par des espaces
            date_heure = date_heure.replace('\n', ' ')
            data['date_heure'] = date_heure.replace("à", "").strip()  # Supprimer "Dernier relevé" et les sauts de ligne
            data['temperature_air'] = sonde.find(class_='temperature').find_all(class_='infowindow-result')[0].text.strip()
            data['temperature_eau'] = sonde.find(class_='temperature').find_all(class_='infowindow-result')[1].text.strip()
            data['salinite_surface'] = sonde.find(class_='salt').find_all(class_='infowindow-result')[0].text.strip()
            data['salinite_milieu'] = sonde.find(class_='salt').find_all(class_='infowindow-result')[1].text.strip()
            data['salinite_fond'] = sonde.find(class_='salt').find_all(class_='infowindow-result')[2].text.strip()
            stations_data.append(data)

        return stations_data
    else:
        # Afficher un message d'erreur si la requête a échoué
        print("Erreur lors de la requête :", response.status_code)
        return None

# Fonction pour enregistrer les données dans un fichier texte
def save_to_file(data, file_path):
    with open(file_path, 'a') as f:
        # En-tête du fichier
        f.write("stations;date_heure;température_air;température_eau;salinité_surface;salinité_milieu;salinité_fond\n")
        for entry in data:
            # Formatage de chaque ligne avec les données
            line = ';'.join([entry['sonde'], entry['date_heure'],
                             entry['temperature_air'], entry['temperature_eau'], entry['salinite_surface'],
                             entry['salinite_milieu'], entry['salinite_fond']])
            f.write(line + '\n')

# URL du site à scraper
url = "https://etangdeberre.org/comprendre/etat-ecologique-de-letang-de-berre/donnees-en-direct/"

# Chemin où enregistrer le fichier texte dans Google Drive
file_path = "etang_de_berre_data.txt"

# Récupérer les données de la page
if station_data:
    # Enregistrer les données dans le fichier texte
    save_to_file(station_data, file_path)
    print("Données enregistrées avec succès.")
else:
    print("Impossible de récupérer les données.")
