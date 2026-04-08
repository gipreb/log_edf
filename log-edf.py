import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "http://etangdeberre.org/comprendre/etat-ecologique-etang-de-berre/donnees-en-direct/"
FILE_NAME = "donnees_etang_berre.csv"

def get_salinity_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    all_rows = []

    # On cible les balises SA1 et SA3
    # Note : Sur le site, elles sont souvent dans des blocs identifiés par leur nom
    balises = ["SA1", "SA3"]
    profondeurs = ["Surface", "Milieu", "Fond"]

    # On cherche dans le texte pour localiser les blocs de données
    for balise in balises:
        # On cherche l'élément qui contient le nom de la balise
        balise_section = soup.find(text=lambda t: balise in t if t else False)
        
        if balise_section:
            # On remonte au parent qui contient les données de cette balise
            parent = balise_section.find_parent("div") 
            
            # On extrait les valeurs (ceci est une simulation de logique, 
            # à ajuster selon les sélecteurs réels du site)
            # Souvent les valeurs sont dans des <span> ou des <td> après le texte "Salinité"
            # Ici, on crée une ligne par balise avec les 3 profondeurs
            row = {
                "Date": timestamp,
                "Balise": balise,
                "Salinité_Surface": None,
                "Salinité_Milieu": None,
                "Salinité_Fond": None
            }
            
            # Exemple de recherche ciblée :
            values = parent.find_all(text=lambda t: "psu" in t.lower() if t else False)
            if len(values) >= 3:
                row["Salinité_Surface"] = values[0].strip()
                row["Salinité_Milieu"] = values[1].strip()
                row["Salinité_Fond"] = values[2].strip()
            
            all_rows.append(row)

    return all_rows

def save_data(data_list):
    df = pd.DataFrame(data_list)
    if not os.path.isfile(FILE_NAME):
        df.to_csv(FILE_NAME, index=False, sep=';', encoding='utf-8')
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False, sep=';', encoding='utf-8')

if __name__ == "__main__":
    data = get_salinity_data()
    if data:
        save_data(data)
        print(f"Enregistrement effectué pour {len(data)} balises.")
