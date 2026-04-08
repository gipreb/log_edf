import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "http://etangdeberre.org/comprendre/etat-ecologique-etang-de-berre/donnees-en-direct/"
FILE_NAME = "donnees_salinite.csv"

def scrape_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # On cherche les blocs de texte contenant "Sonde" ou les listes de données
    # Note : Le sélecteur exact dépend de la structure HTML précise (div, span, etc.)
    data = {
        "date_releve": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "station": "SA1", # Exemple pour une station
        "salinite_surface": None,
        "salinite_fond": None
    }
    
    # Logique d'extraction (à adapter selon les balises du site)
    # Exemple théorique basé sur le texte du site :
    rows = soup.find_all("li")
    for row in rows:
        text = row.get_text()
        if "Salinité" in text:
            # Extraction des chiffres par exemple "Surface : 15,2"
            # On pourrait utiliser des expressions régulières (re) ici
            data["details"] = text.strip()
            
    return data

def save_to_csv(new_data):
    df = pd.DataFrame([new_data])
    if not os.path.isfile(FILE_NAME):
        df.to_csv(FILE_NAME, index=False)
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False)

if __name__ == "__main__":
    try:
        entry = scrape_data()
        save_to_csv(entry)
        print("Données enregistrées avec succès.")
    except Exception as e:
        print(f"Erreur : {e}")
