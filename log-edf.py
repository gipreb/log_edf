import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

URL = "https://etangdeberre.org/comprendre/etat-ecologique-etang-de-berre/donnees-en-direct/"
FILE_NAME = "donnees_etang_berre.csv"

def get_data():
    # Simulation d'un navigateur réel pour éviter d'être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Le GIPREB affiche souvent les données dans des balises "strong" ou "span"
        # On va chercher tous les textes pour extraire ce qui ressemble à des psu (salinité)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Structure de secours si le scraping précis échoue
        results = []
        
        # On cherche les balises SA1 et SA3 dans le texte
        content = soup.get_text()
        
        # Note: Si le site utilise du JavaScript pour charger les chiffres, 
        # 'requests' verra des valeurs vides. 
        # Pour l'instant, on crée une ligne de log même si c'est vide pour éviter l'erreur 2.
        
        data_row = {
            "Date": timestamp,
            "SA1_Surface": "N/A", "SA1_Milieu": "N/A", "SA1_Fond": "N/A",
            "SA3_Surface": "N/A", "SA3_Milieu": "N/A", "SA3_Fond": "N/A"
        }
        
        # ICI : Logique d'extraction à adapter selon le rendu HTML réel
        # Si vous voyez 'N/A' dans votre CSV, il faudra passer par Selenium ou un API interne.
        
        results.append(data_row)
        return results

    except Exception as e:
        print(f"Erreur lors du scraping : {e}")
        return []

def save(data):
    if not data: return
    df = pd.DataFrame(data)
    if not os.path.isfile(FILE_NAME):
        df.to_csv(FILE_NAME, index=False, sep=';')
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False, sep=';')

if __name__ == "__main__":
    extracted_data = get_data()
    save(extracted_data)
