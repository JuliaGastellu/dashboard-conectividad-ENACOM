import streamlit as st
import pandas as pd
import requests
import plotly.express as px


st.set_page_config(layout='wide')

mapa_conectividad = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/mapa_conectividad.csv')
penetracion_hogares = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/Penetracion-hogares.csv')

st.sidebar.title('Filtros')

Provincias = sorted(list(mapa_conectividad['Provincia'].unique()))

# Crear dos columnas
col1, col2 = st.columns([1, 1])

def crear_grafico(df, provincia):
    
    df_filtrado = mapa_conectividad[mapa_conectividad['Provincia'].isin([provincia])]
    
    fig = px.scatter_geo(df_filtrado,
                        lat='Latitud',
                        lon='Longitud',
                        scope='south america',
                        color='Población',  
                        color_continuous_scale='Viridis', 
                        size='Población',
                        hover_name='Provincia',
                        hover_data=['Población'],
                        title='Conectividad a Internet por Provincia',
                        template='plotly_dark'  # Mapa base oscuro
                       )

    # Personalizar el mapa
    fig.update_layout(
        geo=dict(
            showcountries=True,
            countrycolor="LightPink",
            showframe=False,
            showcoastlines=False,
            projection_type="orthographic"
        )
    )

    return fig

# Crear el gráfico de mapa
provincia_seleccionada = st.selectbox("Selecciona una provincia", Provincias)
graf_mapa = crear_grafico(mapa_conectividad, provincia_seleccionada)

with col1: 
    st.plotly_chart(graf_mapa, use_container_width=True)
   

# Obtener los años únicos del DataFrame
años_unicos = penetracion_hogares['Año'].unique()

# Crear un widget de selección para el año
año_seleccionado = st.sidebar.selectbox('Selecciona un año', años_unicos)

# Filtrar los datos por año seleccionado
df_filtrado = penetracion_hogares[penetracion_hogares['Año'] == año_seleccionado]

# Agrupar los datos por Provincia y calcular el promedio
df_agrupado = df_filtrado.groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

def crear_grafico2(df, color_column="Provincia"):
    fig = px.bar(  # Cambiamos a un gráfico de barras para mejor visualización
        df,
        x="Provincia",
        y="Accesos por cada 100 hogares",
        color=color_column,
        title=f"Penetración de hogares en {año_seleccionado}"
    )
    return fig

# Crear el gráfico utilizando la función con el año seleccionado y la columna de color
graf_lineas = crear_grafico2(df_agrupado, color_column="Provincia")

with col2:
    st.plotly_chart(graf_lineas)

