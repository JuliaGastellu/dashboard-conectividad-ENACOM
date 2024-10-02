import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Obtener las provincias únicas
provincias_unicas = penetracion_hogares['Provincia'].unique()

def crear_grafico_mapa(df, provincia):
    # Filtrar los datos por la provincia seleccionada
    df_filtrado = df[df['Provincia'] == provincia]

    # Crear el gráfico de mapa
    fig = px.choropleth(df_filtrado, 
                       locations='Provincia',
                       locationmode='USA-states',  # Ajusta según tu mapa
                       color='Accesos por cada 100 hogares',
                       color_continuous_scale="Viridis",
                       scope="usa",  # Ajusta según tu mapa
                       hover_name="Provincia",
                       title=f'Penetración de hogares en {provincia}')
    return fig