import streamlit as st
import pandas as pd
import grafico_mapa as graf1

st.set_page_config(layout = 'wide')

mapa_conectividad = pd.read_csv("C:/Users/jugas/Proyecto_PIDA/dashboard-conectividad-ENACOM/data/mapa_conectividad.csv")

st.sidebar.title('Filtros')

Provincias = sorted(list(mapa_conectividad['Provincia'].unique()))


#Llamar a los gráficos
graf_mapa = graf1.crear_grafico(mapa_conectividad)