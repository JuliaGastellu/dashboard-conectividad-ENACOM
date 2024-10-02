import pandas as pd
import plotly.express as px

mapa_conectividad = pd.read_csv("C:/Users/jugas/Proyecto_PIDA/dashboard-conectividad-ENACOM/data/mapa_conectividad.csv")

def crear_grafico(df):
	df_mapa = mapa_conectividad.groupby('Provincia').agg({
	
        'Población' : 'sum',
		'Latitud': 'mean',
		'Longitud': 'mean'
	}).reset_index().sort_values(by='Provincia', ascending=False)

	graf_mapa = px.scatter_geo(df_mapa,
		lat = 'Latitud',
		lon = 'Longitud',
		scope = 'south america',
		template = 'seaborn',
		size = 'Población',
		hover_name = 'Provincia',
		hover_data = {'Latitud':False, 'Longitud':False},
		title = 'Población con acceso a internet por Provincia',
	)

	return graf_mapa

