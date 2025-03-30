import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import plotly.subplots as make_subplots
import joblib
import logging
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Conectividad ENACOM",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

# Configuración de estilo
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    """Cargar datos desde archivos parquet."""
    try:
        datasets = {}
        for file in DATA_DIR.glob('*.parquet'):
            name = file.stem
            datasets[name] = pd.read_parquet(file)
            # Crear columna de fecha si no existe
            if 'fecha' not in datasets[name].columns:
                datasets[name]['fecha'] = pd.to_datetime(
                    datasets[name]['año'].astype(str) + '-' + 
                    (datasets[name]['trimestre'] * 3).astype(str).str.zfill(2) + '-01'
                )
        return datasets
    except Exception as e:
        logger.error(f"Error al cargar datos: {str(e)}")
        st.error("Error al cargar los datos. Por favor, verifica que los archivos existan.")
        return None

# Cargar datos
datos = load_data()

# Sidebar
st.sidebar.title('Navegación')
page = st.sidebar.radio('Seleccione una página:', ['Dashboard Principal', 'Análisis Detallado', 'Predicciones'])

if page == 'Dashboard Principal':
    st.title('🌐 Dashboard de Conectividad en Argentina')
    
    # Filtros
    st.sidebar.title('Filtros')
    fecha_max = datos['Internet_Velocidad_Media_de_Descarga_Totales']['fecha'].max()
    fecha_min = datos['Internet_Velocidad_Media_de_Descarga_Totales']['fecha'].min()
    fecha_seleccionada = st.sidebar.date_input(
        'Seleccione una fecha',
        value=fecha_max,
        min_value=fecha_min,
        max_value=fecha_max
    )
    
    # KPIs principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        velocidad_actual = datos['Internet_Velocidad_Media_de_Descarga_Totales'][datos['Internet_Velocidad_Media_de_Descarga_Totales']['fecha'] == fecha_seleccionada]['mbps_(media_de_bajada)'].iloc[0]
        velocidad_anterior = datos['Internet_Velocidad_Media_de_Descarga_Totales'][datos['Internet_Velocidad_Media_de_Descarga_Totales']['fecha'] == fecha_seleccionada - pd.DateOffset(years=1)]['mbps_(media_de_bajada)'].iloc[0]
        cambio_velocidad = ((velocidad_actual - velocidad_anterior) / velocidad_anterior) * 100
        create_kpi_card("Velocidad Media (Mbps)", f"{velocidad_actual:.1f}", cambio_velocidad)
    
    with col2:
        penetracion_actual = datos['Internet_Penetración_Provincias'][datos['Internet_Penetración_Provincias']['fecha'] == fecha_seleccionada]['accesos_cada_100_habitantes'].mean()
        penetracion_anterior = datos['Internet_Penetración_Provincias'][datos['Internet_Penetración_Provincias']['fecha'] == fecha_seleccionada - pd.DateOffset(years=1)]['accesos_cada_100_habitantes'].mean()
        cambio_penetracion = ((penetracion_actual - penetracion_anterior) / penetracion_anterior) * 100
        create_kpi_card("Penetración Promedio", f"{penetracion_actual:.1f}", cambio_penetracion)
    
    with col3:
        ingresos_actual = datos['Internet_Ingresos'][datos['Internet_Ingresos']['fecha'] == fecha_seleccionada]['ingresos'].iloc[0]
        ingresos_anterior = datos['Internet_Ingresos'][datos['Internet_Ingresos']['fecha'] == fecha_seleccionada - pd.DateOffset(years=1)]['ingresos'].iloc[0]
        cambio_ingresos = ((ingresos_actual - ingresos_anterior) / ingresos_anterior) * 100
        create_kpi_card("Ingresos del Sector", f"${ingresos_actual/1e6:.1f}M", cambio_ingresos)
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolución de la velocidad media de descarga
        fig_velocidad = px.line(
            datos['Internet_Velocidad_Media_de_Descarga_Totales'],
            x='fecha',
            y='mbps_(media_de_bajada)',
            title='Evolución de la Velocidad Media de Descarga',
            labels={'mbps_(media_de_bajada)': 'Velocidad (Mbps)', 'fecha': 'Fecha'}
        )
        st.plotly_chart(fig_velocidad, use_container_width=True)
    
    with col2:
        # Distribución de tecnologías
        datos_actuales = datos['Internet_Accesos_Tecnologia_Totales'][datos['Internet_Accesos_Tecnologia_Totales']['fecha'] == fecha_seleccionada]
        fig_tecnologias = px.pie(
            datos_actuales,
            values='total',
            names='tecnologia',
            title='Distribución de Tecnologías de Acceso'
        )
        st.plotly_chart(fig_tecnologias, use_container_width=True)
    
    # Mapa de penetración por provincia
    st.subheader('Penetración de Internet por Provincia')
    datos_mapa = datos['Internet_Penetración_Provincias'][datos['Internet_Penetración_Provincias']['fecha'] == fecha_seleccionada]
    fig_mapa = px.choropleth(
        datos_mapa,
        locations='provincias',
        locationmode='country names',
        color='accesos_cada_100_habitantes',
        title=f'Penetración de Internet por Provincia ({fecha_seleccionada})',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    # Distribución de velocidades
    st.subheader('Distribución de Velocidades por Rango')
    datos_velocidades = datos['Internet_Accesos_Velocidad_Rango_Provincias'][datos['Internet_Accesos_Velocidad_Rango_Provincias']['fecha'] == fecha_seleccionada]
    fig_velocidades = px.bar(
        datos_velocidades,
        x='rango_velocidad',
        y='total',
        color='provincia',
        title='Distribución de Velocidades por Provincia',
        barmode='group'
    )
    st.plotly_chart(fig_velocidades, use_container_width=True)

elif page == 'Análisis Detallado':
    st.title('📊 Análisis Detallado')
    
    # Análisis de correlación
    st.subheader('Correlación entre Variables')
    datos_correlacion = datos['Internet_Velocidad_Media_de_Descarga_Provincias'].merge(
        datos['Internet_Penetración_Provincias'],
        on=['fecha', 'provincia'],
        how='inner'
    )
    corr_matrix = datos_correlacion.select_dtypes(include=[np.number]).corr()
    fig_corr = px.imshow(
        corr_matrix,
        title='Matriz de Correlación entre Variables',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Análisis temporal
    st.subheader('Análisis Temporal')
    col1, col2 = st.columns(2)
    
    with col1:
        # Tendencias de penetración
        fig_tendencia = px.line(
            datos['Internet_Penetración_Provincias'],
            x='fecha',
            y='accesos_cada_100_habitantes',
            color='provincia',
            title='Tendencia de Penetración por Provincia'
        )
        st.plotly_chart(fig_tendencia, use_container_width=True)
    
    with col2:
        # Tendencias de velocidad
        fig_vel_tendencia = px.line(
            datos['Internet_Velocidad_Media_de_Descarga_Provincias'],
            x='fecha',
            y='mbps_(media_de_bajada)',
            color='provincia',
            title='Tendencia de Velocidad por Provincia'
        )
        st.plotly_chart(fig_vel_tendencia, use_container_width=True)
    
    # Análisis de tecnologías
    st.subheader('Evolución de Tecnologías')
    datos_tecnologias = datos['Internet_Accesos_Tecnologia_Provincias'][datos['Internet_Accesos_Tecnologia_Provincias']['fecha'] == fecha_seleccionada]
    fig_tec_evolucion = px.bar(
        datos_tecnologias,
        x='provincia',
        y='total',
        color='tecnologia',
        title='Distribución de Tecnologías por Provincia',
        barmode='stack'
    )
    st.plotly_chart(fig_tec_evolucion, use_container_width=True)

else:
    st.title('📊 Predicciones')
    
    # Cargar modelo
    @st.cache_data
    def load_model():
        """Cargar modelo entrenado."""
        try:
            model = joblib.load(MODEL_DIR / 'best_model.joblib')
            scaler = joblib.load(MODEL_DIR / 'scaler.joblib')
            return model, scaler
        except Exception as e:
            logger.error(f"Error al cargar modelo: {str(e)}")
            return None, None

    model, scaler = load_model()
    if not model or not scaler:
        st.error("No se pudo cargar el modelo. Por favor, ejecuta primero el entrenamiento.")
        return
    
    # Formulario de predicción
    st.subheader("Predicción de Velocidad")
    col1, col2 = st.columns(2)
    
    with col1:
        penetracion = st.number_input(
            "Penetración (accesos cada 100 habitantes)",
            min_value=0.0,
            max_value=100.0,
            value=50.0
        )
        adsl = st.number_input(
            "ADSL (%)",
            min_value=0.0,
            max_value=100.0,
            value=30.0
        )
        cablemodem = st.number_input(
            "Cablemodem (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0
        )
    
    with col2:
        fibra_optica = st.number_input(
            "Fibra Óptica (%)",
            min_value=0.0,
            max_value=100.0,
            value=30.0
        )
        wireless = st.number_input(
            "Wireless (%)",
            min_value=0.0,
            max_value=100.0,
            value=15.0
        )
        otros = st.number_input(
            "Otros (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0
        )
    
    if st.button("Predecir"):
        # Preparar datos para predicción
        features = np.array([[
            penetracion,
            adsl,
            cablemodem,
            fibra_optica,
            wireless,
            otros,
            datetime.now().month,
            datetime.now().quarter,
            datetime.now().year
        ]])
        
        # Escalar características
        features_scaled = scaler.transform(features)
        
        # Realizar predicción
        prediction = model.predict(features_scaled)[0]
        
        # Mostrar resultado
        st.success(f"Velocidad predicha: {prediction:.1f} Mbps")
        
        # Gráfico de barras con la predicción
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Velocidad Predicha'],
            y=[prediction],
            marker_color='#1f77b4'
        ))
        fig.update_layout(
            title='Predicción de Velocidad',
            yaxis_title='Mbps',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

def create_kpi_card(title, value, change=None):
    """Crear tarjeta de KPI."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            {f'<div style="color: {"green" if change > 0 else "red"}">{change:+.1f}%</div>' if change is not None else ''}
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()