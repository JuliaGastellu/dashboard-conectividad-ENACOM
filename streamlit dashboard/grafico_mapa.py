import pandas as pd
import plotly.express as px

# Cargar los datos
mapa_conectividad = pd.read_csv("C:/Users/jugas/Proyecto_PIDA/dashboard-conectividad-ENACOM/data/mapa_conectividad.csv")

def crear_grafico(df):
    # Agrupar y calcular estadísticas
    df_mapa = mapa_conectividad.groupby('Provincia').agg({
        'Población': 'sum',
        'Latitud': 'mean',
        'Longitud': 'mean',
      
    }).reset_index()

    # Crear el mapa
    fig = px.scatter_geo(df_mapa,
                        lat='Latitud',
                        lon='Longitud',
                        scope='south america',
                        color='Población',  # Color según el porcentaje conectado
                        color_continuous_scale='Viridis',  # Escala de colores
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

