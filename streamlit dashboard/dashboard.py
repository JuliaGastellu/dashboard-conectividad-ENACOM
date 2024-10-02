import streamlit as st
import pandas as pd
import requests
import grafico_mapa as graf1

st.set_page_config(layout='wide')

mapa_conectividad = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/mapa_conectividad.csv')



#mapa_conectividad = pd.read_csv("C:/Users/jugas/Proyecto_PIDA/dashboard-conectividad-ENACOM/data/mapa_conectividad.csv")

st.sidebar.title('Filtros')

Provincias = sorted(list(mapa_conectividad['Provincia'].unique()))

# Crear dos columnas
col1, col2 = st.columns([2, 2])  # La primera columna ocupa 3 unidades y la segunda 1 

# En la primera columna, mostrar el mapa
with col1:
    graf_mapa = graf1.crear_grafico(mapa_conectividad)
    st.plotly_chart(graf_mapa, use_container_width=True)

# En la segunda columna, puedes agregar otros elementos, como un texto o un gráfico más pequeño
with col2:
    st.header("Información adicional")
    st.write("Aquí puedes agregar texto, otros gráficos o cualquier otro elemento que desees mostrar.")

