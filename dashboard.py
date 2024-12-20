import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(layout='wide')

mapa_conectividad = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/mapa_conectividad.csv')
penetracion_hogares = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/Penetracion-hogares.csv')
penetracion_totales = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/Penetracion_totales.csv')




st.sidebar.title('Filtros')


# Obtener los años únicos y provincias únicas 
años_unicos = penetracion_hogares['Año'].unique() if 'Año' in penetracion_hogares.columns else None
provincias_unicas = sorted(list(mapa_conectividad['Provincia'].unique())) if 'Provincia' in mapa_conectividad.columns else None

# Crear los selectores en la barra lateral
if años_unicos is not None:
    año_seleccionado = st.sidebar.selectbox('Selecciona un año', años_unicos, key="año_selector")
else:
    año_seleccionado = None

if provincias_unicas is not None:
    provincia_seleccionada = st.sidebar.selectbox("Selecciona una provincia", provincias_unicas)
else:
    provincia_seleccionada = None

# Función para filtrar un DataFrame basado en los selectores
def filtrar_dataframe(df, año_seleccionado, provincia_seleccionada):
    df_filtrado = df.copy()
    if año_seleccionado is not None:
        df_filtrado = df_filtrado[df_filtrado['Año'] == año_seleccionado]
    if provincia_seleccionada is not None:
        df_filtrado = df_filtrado[df_filtrado['Provincia'] == provincia_seleccionada]
    return df_filtrado


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
graf_mapa = crear_grafico(mapa_conectividad, provincia_seleccionada)

with col1: 
    st.plotly_chart(graf_mapa, use_container_width=True)
  # Obtener los años únicos del DataFrame
años_unicos = penetracion_hogares['Año'].unique()


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

# Filtrar los datos por año seleccionado
df_filtrado = penetracion_hogares[penetracion_hogares['Año'] == año_seleccionado]

# Agrupar los datos por Provincia y calcular el promedio
df_agrupado = df_filtrado.groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

def crear_grafico2(df, color_column="Provincia"):
    fig = px.bar(  
        df,
        x="Provincia",
        y="Accesos por cada 100 hogares",
        color=color_column,
        title=f"Penetración de hogares en {año_seleccionado}"
    )
    return fig

# Crear el gráfico utilizando la función con el año seleccionado y la columna de color
graf_lineas = crear_grafico2(df_agrupado, color_column="Provincia")

# Agrupar los datos por año y calcular la suma
df_agrupado = penetracion_totales[penetracion_totales['Año'] != 2024].groupby('Año').sum()

# Crear el gráfico de líneas
fig = px.line(
    df_agrupado,
    x=df_agrupado.index,
    y=['Accesos por cada 100 hogares', 'Accesos por cada 100 hab'],
    title='Suma de accesos por cada 100 hogares y 100 habitantes por año',
    labels={'value': 'Suma de Accesos', 'variable': 'Tipo de Acceso'}
)

# Mostrar el gráfico
st.plotly_chart(fig)

# Crear una tabla pivote
tecnologias = ['ADSL', 'Cablemódem', 'Dial Up', 'Fibra óptica', 'Satelital', 'Wireless', 'Telefonía Fija', '3G', '4G']
df_tecnologias = mapa_conectividad[['Provincia'] + tecnologias]

# Crear una tabla pivot para sumar los valores booleanos por provincia y tecnología
tabla_pivot = pd.pivot_table(df_tecnologias, values=tecnologias, index='Provincia', aggfunc='sum')

# Crear una tabla pivote
#tabla_pivot = mapa_conectividad.pivot_table(index='Provincia', columns='tecnologia_seleccionada', values='cantidad_accesos', aggfunc='sum')

colors = px.colors.qualitative.G10  # Paleta de 10 colores

# Crear el gráfico de barras apiladas con Plotly
fig = go.Figure(data=[
    go.Bar(
        name=col,
        x=tabla_pivot.index,
        y=tabla_pivot[col],
        marker_color=colors[i]  # Asigna un color de la lista a cada barra
    ) for i, col in enumerate(tabla_pivot.columns)
])

# Personalizar el gráfico
fig.update_layout(
    title='Distribución de tecnologías por provincia',
    xaxis_title='Provincia',
    yaxis_title='Cantidad de localidades'
)

# Mostrar el gráfico
fig.show()

st.plotly_chart(fig)

tabla_pivot = mapa_conectividad.groupby('Provincia')[tecnologias + ['Población']].sum()

# Crear un gráfico de barras apiladas con Plotly
fig = go.Figure(data=[
    go.Bar(
        name=col,
        x=tabla_pivot.index,
        y=tabla_pivot[col],
        marker_color=colors[i]
    ) for i, col in enumerate(tecnologias)
])

# Agregar una traza adicional para la población total
fig.add_trace(go.Bar(
    name='Población Total',
    x=tabla_pivot.index,
    y=tabla_pivot['Población'],
    marker_color='black'
))

# Personalizar el gráfico
fig.update_layout(
    title='Población con acceso a cada tecnología por provincia',
    xaxis_title='Provincia',
    yaxis_title='Población',
    barmode='stack'  # Asegurarse de que las barras estén apiladas
)

# Mostrar el gráfico
fig.show()


st.plotly_chart(fig)