import pandas as pd

old_data = pd.read_csv('hourlyQuebecEDStats.csv')
old_data['Mise_a_jour'] = pd.to_datetime(old_data['Mise_a_jour'])
old_data["Heure_de_l'extraction_(image)"] = pd.to_datetime(
    old_data["Heure_de_l'extraction_(image)"])
print('old data: ', len(old_data))

new_data = pd.read_csv(
    'https://www.msss.gouv.qc.ca/professionnels/statistiques/documents/urgences/Releve_horaire_urgences_7jours.csv', encoding="ISO-8859-1")

new_data.rename(columns=lambda x: x.strip(), inplace=True)
new_data['Mise_a_jour'] = pd.to_datetime(new_data['Mise_a_jour'])
new_data["Heure_de_l'extraction_(image)"] = pd.to_datetime(
    new_data["Heure_de_l'extraction_(image)"])
new_data['Nombre_de_civieres_fonctionnelles'] = pd.to_numeric(
    new_data['Nombre_de_civieres_fonctionnelles'], errors='coerce')
new_data['Nombre_de_civieres_occupees'] = pd.to_numeric(
    new_data['Nombre_de_civieres_occupees'], errors='coerce')
new_data['Nombre_de_patients_sur_civiere_plus_de_24_heures'] = pd.to_numeric(
    new_data['Nombre_de_patients_sur_civiere_plus_de_24_heures'], errors='coerce')
new_data['Nombre_de_patients_sur_civiere_plus_de_48_heures'] = pd.to_numeric(
    new_data['Nombre_de_patients_sur_civiere_plus_de_48_heures'], errors='coerce')
print('new data: ', len(new_data))

concat_data = pd.concat([old_data, new_data], ignore_index=False)
concat_data = concat_data.drop_duplicates().reset_index(drop=True)
print('concat data: ', len(concat_data))

concat_data.to_csv('hourlyQuebecEDStats.csv', index=False)

new_jgh_hourly = new_data[new_data.No_permis_installation == 12685608]
new_jgh_hourly = new_jgh_hourly[[
    'Nombre_de_civieres_occupees', "Heure_de_l'extraction_(image)"]]
new_jgh_hourly = new_jgh_hourly.rename(
    columns={'Nombre_de_civieres_occupees': 'y', "Heure_de_l'extraction_(image)": 'ds'})
new_jgh_hourly.ds = pd.to_datetime(new_jgh_hourly.ds)

jgh_occupancy = pd.read_csv('jghOccupancy.csv')
jgh_occupancy.ds = pd.to_datetime(jgh_occupancy.ds)

jgh_occupancy = jgh_occupancy.append(
    new_jgh_hourly, ignore_index=True, sort=False)
jgh_occupancy = jgh_occupancy.drop_duplicates()
jgh_occupancy = jgh_occupancy.dropna()
jgh_occupancy.to_csv('jghOccupancy.csv', index=False)
