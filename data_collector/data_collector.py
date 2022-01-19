import requests
from bs4 import BeautifulSoup
import json
import random
import time

url = 'https://arato.inf.unideb.hu/levelezo/index.php'

def get_all_training():

    req = requests.get(url, allow_redirects=True)

    soup = BeautifulSoup(req.text, 'html.parser')
    trainings_bs = soup.find('select', attrs={'name': 'szak'}).find_all('option')

    trainings = {}

    for training in trainings_bs:
        if training.text != '':
            trainings.update({training.attrs['value']: training.text})

    return trainings

def get_training_data(key):
    req = requests.post(url, data={'szak': key, 'tanar': '', 'targy': '', 'terem': '', 'datum': '', 'submit': 'Mehet!'})

    table_bs = BeautifulSoup(req.text, 'html.parser').html.body
    if table_bs.find('h3') != None:
        return []

    table_bs = table_bs.center.table
    rows = table_bs.find_all('tr')
    education_date = ''

    data = []

    for row in rows:
        if row.find('th') != None:
            continue

        cells = row.find_all('td')
        
        if len(cells) == 1:
            education_date = cells[0].text[:cells[0].text.rfind('(') - 1].strip()
        else:
            parts = cells[0].text.split('-')
            subject_parts = cells[3].text.split(' ')

            data.append({
                                    'training': cells[4].text.strip(),
                                    'education_date': education_date,
                                    'time_start': parts[0].strip(),
                                    'time_end': parts[1].strip(),
                                    'lecturer': cells[1].text.strip(),
                                    'classroom': cells[2].text.strip(),
                                    'subject_code': subject_parts[0].strip(),
                                    'subject_type': subject_parts[-1].strip(),
                                    'subject_name': ' '.join(subject_parts[1:-1])[:-1].strip()
                                })
        
    return data

trainings = get_all_training()
consultations = []

for key in trainings:
    waiting_time = random.randint(10, 30)
    time.sleep(waiting_time)
    consultations.extend(get_training_data(key))

for i in consultations:
    print(i)

with open('sample.json', 'w', encoding='utf-8') as f:
    json_string = json.dumps({ 'consultations': consultations}, ensure_ascii=False)
    f.write(json_string)