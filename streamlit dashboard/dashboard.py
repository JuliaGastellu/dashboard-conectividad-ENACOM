import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import grafico_mapa as graf1



st.set_page_config(layout='wide')

mapa_conectividad = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/mapa_conectividad.csv')
penetracion_hogares = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/Penetracion-hogares.csv')

st.sidebar.title('Filtros')

Provincias = sorted(list(mapa_conectividad['Provincia'].unique()))

# Crear dos columnas
col1, col2 = st.columns([1, 1])  # La primera columna ocupa 3 unidades y la segunda 1 

# En la primera columna, mostrar el mapa
with col1: 
    
    graf_mapa = graf1.crear_grafico(mapa_conectividad)
    st.plotly_chart(graf_mapa, use_container_width=True)
   

# Obtener los años únicos del DataFrame
años_unicos = penetracion_hogares['Año'].unique()

# Crear un widget de selección para el año
año_seleccionado = st.sidebar.selectbox('Selecciona un año', años_unicos)

# Filtrar los datos por año seleccionado
df_filtrado = penetracion_hogares[penetracion_hogares['Año'] == año_seleccionado]

# Agrupar los datos por Provincia y calcular el promedio
df_agrupado = df_filtrado.groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

# Función para crear el gráfico de líneas (simplificada)
def crear_grafico2(df, color_column="Provincia"):
    fig = px.scatter(
        df,
        x="Provincia",
        y="Accesos por cada 100 hogares",
        color=color_column,
        size="Accesos por cada 100 hogares",
        hover_name="Provincia",
        title=f"Evolución de la penetración de hogares en {año_seleccionado}"
    )
    return fig

# Crear el gráfico utilizando la función con el año seleccionado y la columna de color
graf_lineas = crear_grafico2(df_agrupado, color_column="Provincia")

with col2:
    st.plotly_chart(graf_lineas)
