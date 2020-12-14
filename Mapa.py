import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Confesiones").sheet1


confesiones_lista = sheet.get_all_records()
# print(confesiones_lista)

import folium

map = folium.Map(location=[-1.4469559866382844, -78.55798865486415], titles="Mapbox Bright", zoom_start=7) # [-90 - 90, -180 - 180], zoom_start=6

fg = folium.FeatureGroup(name="Mi Mapa")

for confesion in confesiones_lista:
    latitud, longitud = confesion['Direccion'].split(',')
    print(latitud)
    print(longitud)
    conf = confesion['Confesion']
    fg.add_child(folium.Marker(location=[latitud, longitud], popup=conf, icon=folium.Icon(color='green')))

map.add_child(fg)

map.save("Map1.html")