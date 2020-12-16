from flask import Flask, render_template

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import time

time.sleep(2)
print('Iniciando aplicación...')

time.sleep(2)
print('Validando credenciales...')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('resources/client_secret.json', scope)
client = gspread.authorize(creds)

time.sleep(4)
print('Importando Anécdotas...')

sheet = client.open("Anecdotas").sheet1

anecdotas_lista = sheet.get_all_records()

import folium

map = folium.Map(location=[-1.4469559866382844, -78.55798865486415], titles="Mapbox Bright", zoom_start=7) # [-90 - 90, -180 - 180], zoom_start=6

fg = folium.FeatureGroup(name="Mi Mapa")

for anecdotas in anecdotas_lista:
    latitud, longitud = anecdotas['Latitud, Longitud'].split(',')
    marcador = anecdotas['Marcador']
    conf = anecdotas['Anécdota']
    fg.add_child(folium.Marker(location=[latitud, longitud], popup=conf, icon=folium.Icon(color=marcador)))

map.add_child(fg)

time.sleep(6)
print('Actualizando mapa...')

map.save("templates/Map1.html")

time.sleep(3)
print("¡Mapa listo!, espere un instante a que se muestre en pantalla")

app = Flask(__name__, template_folder='templates')

@app.route('/')
def handle_request():
  return render_template("Map1.html")  

if __name__=="__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
