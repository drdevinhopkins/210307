import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import time
import os


old_data = pd.read_csv('..data/dailyMontrealEdStats.csv')
old_data['date'] = pd.to_datetime(old_data['date'])
print('old data: ', len(old_data), ' rows, ending ', old_data.date.max())

url = 'https://santemontreal.qc.ca/fileadmin/fichiers_portail/Donnees_urgence/urgence_quotidien_media.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, features="html.parser")

table = soup.find('table')

rows = table.find_all('tr')
table_rows = rows[0].find_all('tr')

columns = [i.text.replace('-', '') for i in table_rows[6].find_all('td')]

df_rows = []
for tr in table_rows[7:][:-6]:
    td = tr.find_all('td')
    row = [i.text for i in td]
    if '\xa0' in str(tr):
        continue
    if 'Sous-total' in str(tr):
        continue
    df_rows.append(row)

df = pd.DataFrame.from_records(df_rows, columns=columns)

columns.remove('Installation')

for int_col in columns:
    df[int_col] = pd.to_numeric(df[int_col], errors='coerce')

yesterday = date.today() - timedelta(days=1)
df['date'] = yesterday
df.date = pd.to_datetime(df.date)

new_data = df

print('new data: ', len(new_data), ' rows, ending ', new_data.date.max())

concat_data = pd.concat([old_data, new_data], ignore_index=False)
concat_data = concat_data.drop_duplicates().reset_index(drop=True)
print('concat data: ', len(concat_data), ' rows')

concat_data.to_csv('..data/dailyMontrealEdStats.csv', index=False)

old_jgh_data = pd.read_csv('../data/jghDailyVisits.csv')
old_jgh_data['ds'] = pd.to_datetime(old_jgh_data['ds'])
print('old jgh data: ', len(old_jgh_data),
      ' rows, ending ', old_jgh_data.ds.max())

new_jgh_data = df[df.Installation == "L'Hôpital général juif Sir Mortimer B. Davis"][[
    'Nombre inscriptions', 'date']]

new_jgh_data = new_jgh_data.rename(
    columns={'Nombre inscriptions': "y", "date": "ds"})

concat_jgh_data = old_jgh_data.append(
    new_jgh_data, ignore_index=True, sort=True)

print('concat jgh data: ', len(concat_jgh_data))

concat_jgh_data.to_csv('../data/jghDailyVisits.csv', index=False)
