import pandas as pd
import tabula
from datetime import date, timedelta

df = tabula.read_pdf(
    "https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Rap_Quotid_SituatUrgence1.pdf", pages="7")[0]

new_jgh_last_5 = df.loc[27]['Visites totales la veille'].split(' ')
new_jgh_last_5 = [int(visits) for visits in new_jgh_last_5]

old_jgh_data = pd.read_csv('jghDailyVisits.csv')
old_jgh_data['ds'] = pd.to_datetime(old_jgh_data['ds'])
old_jgh_last_5 = old_jgh_data.y.tail().tolist()

if new_jgh_last_5 != old_jgh_last_5:
    print('new data')
    jgh_visits_yest = new_jgh_last_5[4]
    new_jgh_data = pd.DataFrame(
        [{'ds': pd.to_datetime(date.today()-timedelta(days=1)), 'y': jgh_visits_yest}])
    concat_jgh_data = old_jgh_data.append(
        new_jgh_data, ignore_index=True, sort=True)
    concat_jgh_data.to_csv('jghDailyVisits.csv', index=False)
else:
    print('no new data')
