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

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Conectividad - ENACOM",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .insight-card {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Definir directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

def create_kpi_card(title, value, change=None):
    """Crear tarjeta de KPI."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            {f'<div style="color: {"green" if change > 0 else "red"}">{change:+.1f}%</div>' if change is not None else ''}
        </div>
    """, unsafe_allow_html=True)

def create_insight_card(text):
    """Crear tarjeta de insight."""
    st.markdown(f"""
        <div class="insight-card">
            <p>{text}</p>
        </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carga los datos necesarios para el dashboard."""
    try:
        # Cargar datasets
        velocidad = pd.read_parquet(DATA_DIR / 'Internet Velocidad Media de Descarga Provincias.parquet')
        penetracion = pd.read_parquet(DATA_DIR / 'Internet Penetración Provincias.parquet')
        tecnologia = pd.read_parquet(DATA_DIR / 'Internet Accesos Tecnologia Provincias.parquet')
        
        # Limpiar valores numéricos
        velocidad['mbps_(media_de_bajada)'] = velocidad['mbps_(media_de_bajada)'].str.replace(',', '.').astype(float)
        penetracion['accesos_cada_100_habitantes'] = penetracion['accesos_cada_100_habitantes'].str.replace(',', '.').astype(float)
        
        # Crear columna de fecha
        for df in [velocidad, penetracion, tecnologia]:
            df['fecha'] = pd.to_datetime(
                df['año'].astype(str) + '-' + 
                (df['trimestre'] * 3).astype(str).str.zfill(2) + '-01'
            )
        
        # Renombrar columnas de provincia para consistencia
        penetracion = penetracion.rename(columns={'provincias': 'provincia'})
        
        # Corregir nombre de Capital Federal
        for df in [velocidad, penetracion, tecnologia]:
            df['provincia'] = df['provincia'].replace('Capital Federal', 'Ciudad Autónoma de Buenos Aires')
        
        # Merge de datasets
        df = velocidad.merge(
            penetracion,
            on=['fecha', 'provincia'],
            how='inner'
        )
        
        df = df.merge(
            tecnologia,
            on=['fecha', 'provincia'],
            how='inner'
        )
        
        # Calcular métricas adicionales
        df['cambio_velocidad'] = df.groupby('provincia')['mbps_(media_de_bajada)'].pct_change()
        df['cambio_penetracion'] = df.groupby('provincia')['accesos_cada_100_habitantes'].pct_change()
        
        # Verificar columnas disponibles
        logger.info(f"Columnas disponibles: {df.columns.tolist()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error al cargar datos: {str(e)}")
        return None

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

def show_dashboard_principal(df):
    """Mostrar dashboard principal."""
    try:
        st.title("🌐 Dashboard de Conectividad en Argentina")
        
        # Filtros
        st.sidebar.title('Filtros')
        
        # Aclaración sobre trimestres
        st.sidebar.markdown("""
        **Aclaración sobre períodos:**
        - T1: Primer trimestre (Enero-Marzo)
        - T2: Segundo trimestre (Abril-Junio)
        - T3: Tercer trimestre (Julio-Septiembre)
        - T4: Cuarto trimestre (Octubre-Diciembre)
        """)
        
        # Obtener períodos disponibles
        df['periodo'] = df['año'].astype(str) + ' - T' + df['trimestre'].astype(str)
        periodos_disponibles = sorted(df['periodo'].unique())
        
        if len(periodos_disponibles) == 0:
            st.error("No hay datos disponibles para mostrar.")
            return
            
        # Selector de período
        periodo_seleccionado = st.sidebar.selectbox(
            'Seleccione un período',
            options=periodos_disponibles,
            index=len(periodos_disponibles)-1  # Por defecto, mostrar el último período
        )
        
        # Filtrar datos por período seleccionado
        df_filtrado = df[df['periodo'] == periodo_seleccionado]
        
        if df_filtrado.empty:
            st.warning(f"No hay datos disponibles para el período {periodo_seleccionado}")
            return
            
        # Obtener datos del período anterior para comparación
        periodo_anterior = periodos_disponibles[max(0, periodos_disponibles.index(periodo_seleccionado) - 1)]
        df_anterior = df[df['periodo'] == periodo_anterior]
        
        # KPIs principales
        st.subheader(f"📊 Indicadores del Período {periodo_seleccionado}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            velocidad_actual = df_filtrado['mbps_(media_de_bajada)'].mean()
            if not df_anterior.empty:
                velocidad_anterior = df_anterior['mbps_(media_de_bajada)'].mean()
                cambio_velocidad = ((velocidad_actual - velocidad_anterior) / velocidad_anterior) * 100
            else:
                cambio_velocidad = None
            create_kpi_card("Velocidad Media (Mbps)", f"{velocidad_actual:.1f}", cambio_velocidad)
        
        with col2:
            penetracion_actual = df_filtrado['accesos_cada_100_habitantes'].mean()
            if not df_anterior.empty:
                penetracion_anterior = df_anterior['accesos_cada_100_habitantes'].mean()
                cambio_penetracion = ((penetracion_actual - penetracion_anterior) / penetracion_anterior) * 100
            else:
                cambio_penetracion = None
            create_kpi_card("Penetración Promedio", f"{penetracion_actual:.1f}", cambio_penetracion)
        
        with col3:
            total_accesos = df_filtrado['total'].sum()
            if not df_anterior.empty:
                total_anterior = df_anterior['total'].sum()
                cambio_total = ((total_accesos - total_anterior) / total_anterior) * 100
            else:
                cambio_total = None
            create_kpi_card("Total de Accesos", f"{total_accesos/1e6:.1f}M", cambio_total)
        
        # Insights
        st.subheader("📊 Insights Principales")
        col1, col2 = st.columns(2)
        
        with col1:
            # Análisis de velocidad
            if not df_filtrado.empty:
                velocidad_max = df_filtrado['mbps_(media_de_bajada)'].max()
                velocidad_min = df_filtrado['mbps_(media_de_bajada)'].min()
                provincia_max = df_filtrado.loc[df_filtrado['mbps_(media_de_bajada)'].idxmax(), 'provincia']
                provincia_min = df_filtrado.loc[df_filtrado['mbps_(media_de_bajada)'].idxmin(), 'provincia']
                
                create_insight_card(f"""
                    La provincia con mayor velocidad de descarga es {provincia_max} ({velocidad_max:.1f} Mbps),
                    mientras que {provincia_min} tiene la menor velocidad ({velocidad_min:.1f} Mbps).
                    La diferencia es de {velocidad_max - velocidad_min:.1f} Mbps.
                """)
            else:
                st.warning("No hay datos suficientes para mostrar insights de velocidad.")
        
        with col2:
            # Análisis de penetración
            if not df_filtrado.empty:
                penetracion_max = df_filtrado['accesos_cada_100_habitantes'].max()
                penetracion_min = df_filtrado['accesos_cada_100_habitantes'].min()
                provincia_pen_max = df_filtrado.loc[df_filtrado['accesos_cada_100_habitantes'].idxmax(), 'provincia']
                provincia_pen_min = df_filtrado.loc[df_filtrado['accesos_cada_100_habitantes'].idxmin(), 'provincia']
                
                create_insight_card(f"""
                    {provincia_pen_max} tiene la mayor penetración de internet ({penetracion_max:.1f} accesos/100 hab),
                    mientras que {provincia_pen_min} tiene la menor ({penetracion_min:.1f} accesos/100 hab).
                """)
            else:
                st.warning("No hay datos suficientes para mostrar insights de penetración.")
        
        # Gráficos principales
        st.subheader("📈 Evolución Trimestral")
        col1, col2 = st.columns(2)
        
        with col1:
            if not df.empty:
                # Agrupar por período y calcular promedios
                df_evol = df.groupby('periodo').agg({
                    'mbps_(media_de_bajada)': 'mean',
                    'accesos_cada_100_habitantes': 'mean'
                }).reset_index()
                
                fig_velocidad = px.line(
                    df_evol,
                    x='periodo',
                    y='mbps_(media_de_bajada)',
                    title='Evolución de la Velocidad Media',
                    labels={'mbps_(media_de_bajada)': 'Velocidad (Mbps)', 'periodo': 'Período'}
                )
                st.plotly_chart(fig_velocidad, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para mostrar la evolución de velocidad.")
        
        with col2:
            if not df.empty:
                fig_penetracion = px.line(
                    df_evol,
                    x='periodo',
                    y='accesos_cada_100_habitantes',
                    title='Evolución de la Penetración',
                    labels={'accesos_cada_100_habitantes': 'Accesos/100 hab', 'periodo': 'Período'}
                )
                st.plotly_chart(fig_penetracion, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para mostrar la evolución de penetración.")
        
        # Distribución de tecnologías
        st.subheader("📱 Distribución de Tecnologías")
        col1, col2 = st.columns(2)
        
        with col1:
            # Verificar columnas disponibles para tecnologías
            tech_columns = [col for col in df.columns if col in ['adsl', 'cablemodem', 'fibra_optica', 'wireless', 'otros']]
            if tech_columns and not df_filtrado.empty:
                tech_data = df_filtrado[tech_columns].sum()
                fig_tecnologias = px.pie(
                    values=tech_data.values,
                    names=tech_data.index,
                    title=f'Distribución de Tecnologías - {periodo_seleccionado}',
                    hole=0.3
                )
                st.plotly_chart(fig_tecnologias, use_container_width=True)
            else:
                st.warning("No se encontraron datos de tecnologías disponibles.")
        
        with col2:
            if tech_columns and not df.empty:
                # Agrupar por período y sumar tecnologías
                tech_evol = df.groupby('periodo')[tech_columns].sum().reset_index()
                fig_tecnologias_evol = px.line(
                    tech_evol,
                    x='periodo',
                    y=tech_columns,
                    title='Evolución de Tecnologías de Acceso',
                    labels={'value': 'Total de Accesos', 'periodo': 'Período'}
                )
                st.plotly_chart(fig_tecnologias_evol, use_container_width=True)
            else:
                st.warning("No se encontraron datos de evolución de tecnologías.")
        
        # Mapa de calor de correlaciones
        st.subheader("🔍 Análisis de Correlaciones")
        if not df_filtrado.empty:
            numeric_cols = df_filtrado.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df_filtrado[numeric_cols].corr()
                fig_corr = px.imshow(
                    corr_matrix,
                    title=f'Matriz de Correlación - {periodo_seleccionado}',
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("No hay suficientes columnas numéricas para mostrar correlaciones.")
        else:
            st.warning("No hay datos disponibles para mostrar correlaciones.")
    
    except Exception as e:
        logger.error(f"Error en show_dashboard_principal: {str(e)}")
        st.error(f"Error al mostrar el dashboard: {str(e)}")

def show_analisis_detallado(df):
    """Mostrar análisis detallado."""
    try:
        st.title("📊 Análisis Detallado")
        
        # Selector de provincia
        provincias = sorted(df['provincia'].unique())
        provincia_seleccionada = st.selectbox("Seleccionar Provincia", provincias)
        
        # Filtrar datos por provincia
        df_provincia = df[df['provincia'] == provincia_seleccionada]
        
        # KPIs de la provincia
        col1, col2, col3 = st.columns(3)
        
        with col1:
            velocidad_actual = df_provincia['mbps_(media_de_bajada)'].iloc[-1]
            velocidad_anterior = df_provincia['mbps_(media_de_bajada)'].iloc[-2]
            cambio_velocidad = ((velocidad_actual - velocidad_anterior) / velocidad_anterior) * 100
            create_kpi_card("Velocidad Actual", f"{velocidad_actual:.1f} Mbps", cambio_velocidad)
        
        with col2:
            penetracion_actual = df_provincia['accesos_cada_100_habitantes'].iloc[-1]
            penetracion_anterior = df_provincia['accesos_cada_100_habitantes'].iloc[-2]
            cambio_penetracion = ((penetracion_actual - penetracion_anterior) / penetracion_anterior) * 100
            create_kpi_card("Penetración Actual", f"{penetracion_actual:.1f}", cambio_penetracion)
        
        with col3:
            total_actual = df_provincia['total'].iloc[-1]
            total_anterior = df_provincia['total'].iloc[-2]
            cambio_total = ((total_actual - total_anterior) / total_anterior) * 100
            create_kpi_card("Total Accesos", f"{total_actual/1e3:.1f}K", cambio_total)
        
        # Gráficos por provincia
        col1, col2 = st.columns(2)
        
        with col1:
            fig_velocidad_prov = px.line(
                df_provincia,
                x='fecha',
                y='mbps_(media_de_bajada)',
                title=f'Velocidad Media en {provincia_seleccionada}',
                markers=True
            )
            st.plotly_chart(fig_velocidad_prov, use_container_width=True)
        
        with col2:
            fig_penetracion_prov = px.line(
                df_provincia,
                x='fecha',
                y='accesos_cada_100_habitantes',
                title=f'Penetración en {provincia_seleccionada}',
                markers=True
            )
            st.plotly_chart(fig_penetracion_prov, use_container_width=True)
        
        # Distribución de tecnologías por provincia
        st.subheader("📱 Distribución de Tecnologías")
        tech_columns = [col for col in df.columns if col in ['adsl', 'cablemodem', 'fibra_optica', 'wireless', 'otros']]
        if tech_columns:
            tech_data = df_provincia[tech_columns].iloc[-1]
            fig_tecnologias_prov = px.bar(
                x=tech_data.index,
                y=tech_data.values,
                title=f'Distribución de Tecnologías en {provincia_seleccionada}',
                labels={'x': 'Tecnología', 'y': 'Total de Accesos'}
            )
            st.plotly_chart(fig_tecnologias_prov, use_container_width=True)
        else:
            st.warning("No se encontraron datos de tecnologías disponibles para esta provincia.")
    
    except Exception as e:
        logger.error(f"Error en show_analisis_detallado: {str(e)}")
        st.error(f"Error al mostrar el análisis detallado: {str(e)}")

def show_prediction_section(df):
    """Mostrar sección de predicciones."""
    try:
        st.title("🔮 Simulador de Velocidad de Internet")
        st.markdown("""
        Esta herramienta te permite simular cómo diferentes combinaciones de tecnologías y niveles de penetración 
        podrían afectar la velocidad media de descarga en una provincia.
        """)
        
        # Selector de provincia
        provincias = sorted(df['provincia'].unique())
        provincia_seleccionada = st.selectbox("Seleccionar Provincia", provincias)
        
        # Obtener datos históricos de la provincia seleccionada
        df_provincia = df[df['provincia'] == provincia_seleccionada].iloc[-1]
        
        # Mostrar datos actuales de la provincia
        st.subheader("📊 Datos Actuales de la Provincia")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Velocidad Actual",
                f"{df_provincia['mbps_(media_de_bajada)']:.1f} Mbps"
            )
            st.metric(
                "Penetración Actual",
                f"{df_provincia['accesos_cada_100_habitantes']:.1f} accesos/100 hab"
            )
        
        with col2:
            # Calcular distribución actual de tecnologías
            tech_columns = [col for col in df.columns if col in ['adsl', 'cablemodem', 'fibra_optica', 'wireless', 'otros']]
            if tech_columns:
                tech_data = df_provincia[tech_columns]
                total_tech = tech_data.sum()
                tech_percentages = (tech_data / total_tech * 100).round(1)
                
                for tech, percentage in tech_percentages.items():
                    st.metric(
                        f"{tech.replace('_', ' ').title()}",
                        f"{percentage:.1f}%"
                    )
        
        # Simulador
        st.subheader("🎯 Simulador de Escenarios")
        st.markdown("""
        Ajusta los valores para simular diferentes escenarios y ver cómo podrían afectar la velocidad de internet.
        Los valores se ajustan automáticamente para mantener un total del 100%.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sliders para tecnologías
            tech_values = {}
            total_percentage = 0
            
            for tech in tech_columns:
                current_value = tech_percentages[tech]
                tech_values[tech] = st.slider(
                    f"{tech.replace('_', ' ').title()} (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(current_value),
                    step=0.1,
                    key=f"slider_{tech}"
                )
                total_percentage += tech_values[tech]
            
            # Ajustar valores para mantener 100%
            if total_percentage != 100:
                adjustment = 100 - total_percentage
                for tech in tech_columns:
                    tech_values[tech] += adjustment / len(tech_columns)
        
        with col2:
            # Slider para penetración
            current_penetration = df_provincia['accesos_cada_100_habitantes']
            penetration = st.slider(
                "Penetración (accesos cada 100 habitantes)",
                min_value=0.0,
                max_value=100.0,
                value=float(current_penetration),
                step=0.1
            )
            
            # Mostrar predicción
            if st.button("Calcular Predicción"):
                try:
                    # Cargar modelo
                    model, scaler = load_model()
                    if not model or not scaler:
                        st.error("No se pudo cargar el modelo. Por favor, ejecuta primero el entrenamiento.")
                        return
                    
                    # Preparar datos para predicción
                    features = np.array([[
                        penetration,
                        tech_values['adsl'],
                        tech_values['cablemodem'],
                        tech_values['fibra_optica'],
                        tech_values['wireless'],
                        tech_values['otros'],
                        datetime.now().month,
                        datetime.now().quarter,
                        datetime.now().year
                    ]])
                    
                    # Escalar características
                    features_scaled = scaler.transform(features)
                    
                    # Realizar predicción
                    prediction = model.predict(features_scaled)[0]
                    
                    # Calcular cambio porcentual
                    current_speed = df_provincia['mbps_(media_de_bajada)']
                    change = ((prediction - current_speed) / current_speed) * 100
                    
                    # Mostrar resultados
                    st.success(f"""
                        **Velocidad Predicha:** {prediction:.1f} Mbps
                        
                        **Cambio respecto a la actual:** {change:+.1f}%
                    """)
                    
                    # Gráfico comparativo
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Actual', 'Predicción'],
                        y=[current_speed, prediction],
                        marker_color=['#1f77b4', '#ff7f0e']
                    ))
                    fig.update_layout(
                        title='Comparación de Velocidades',
                        yaxis_title='Mbps',
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Análisis de impacto
                    st.subheader("📈 Análisis de Impacto")
                    if change > 0:
                        st.info(f"""
                            La combinación propuesta podría mejorar la velocidad en un {change:.1f}%.
                            Esto podría resultar en:
                            - Mejor experiencia de usuario
                            - Mayor capacidad para servicios en línea
                            - Mejor soporte para aplicaciones de alta demanda
                        """)
                    else:
                        st.warning(f"""
                            La combinación propuesta podría reducir la velocidad en un {abs(change):.1f}%.
                            Considera:
                            - Aumentar la proporción de tecnologías más rápidas
                            - Mejorar la infraestructura de red
                            - Evaluar la distribución de tecnologías
                        """)
                
                except Exception as e:
                    logger.error(f"Error en la predicción: {str(e)}")
                    st.error("Error al realizar la predicción. Por favor, verifica los datos ingresados.")
    
    except Exception as e:
        logger.error(f"Error en show_prediction_section: {str(e)}")
        st.error("Error al mostrar la sección de predicciones. Por favor, intente nuevamente más tarde.")

def main():
    """Función principal del dashboard."""
    try:
        # Sidebar
        st.sidebar.title("Navegación")
        page = st.sidebar.radio(
            "Seleccione una página:",
            ["Dashboard Principal", "Análisis Detallado", "Simulador de Velocidad"]
        )
        
        # Cargar datos
        with st.spinner("Cargando datos..."):
            df = load_data()
            if df is None:
                st.error("Error al cargar los datos. Por favor, verifica los archivos de datos.")
                return
        
        if page == "Dashboard Principal":
            show_dashboard_principal(df)
        elif page == "Análisis Detallado":
            show_analisis_detallado(df)
        else:
            show_prediction_section(df)
    
    except Exception as e:
        logger.error(f"Error en el dashboard: {str(e)}")
        st.error("Ha ocurrido un error en el dashboard. Por favor, intente nuevamente más tarde.")

if __name__ == "__main__":
    main()