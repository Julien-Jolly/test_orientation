import requests
from bs4 import BeautifulSoup
import json

q_a = {}

for i in range(5):
    url=f"https://www.letudiant.fr/test/metiers/orientation/pour-quels-metiers-etes-vous-fait/question-{i+1}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('p')
    q = elements[2].get_text().replace('\xa0', ' ').strip()
    r1 = elements[3].get_text().replace('\xa0', ' ').strip()
    r2 = elements[4].get_text().replace('\xa0', ' ').strip()
    q_a[f"question n°{i+1} : {q}"] = {"reponse 1": r1, "reponse 2": r2}

with open("questions.json", "w", encoding="utf-8") as file:
    json.dump(q_a, file, ensure_ascii=False, indent=4)
