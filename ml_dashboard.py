import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import joblib
import logging
from datetime import datetime
from ml_analysis import (
    load_and_prepare_data,
    train_models,
    analyze_feature_importance,
    plot_prediction_vs_actual,
    plot_residuals
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Machine Learning - ENACOM",
    page_icon="🤖",
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
    </style>
    """, unsafe_allow_html=True)

# Definir directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

def main():
    """Función principal del dashboard de ML."""
    try:
        st.title("Análisis de Machine Learning - Conectividad ENACOM")
        
        # Sidebar
        st.sidebar.title("Opciones de Análisis")
        analysis_type = st.sidebar.selectbox(
            "Seleccionar Tipo de Análisis",
            ["Modelos Tradicionales", "Análisis de Residuos"]
        )
        
        # Cargar datos
        with st.spinner("Cargando datos..."):
            X, y, features = load_and_prepare_data()
            if X is None or y is None:
                st.error("Error al cargar los datos. Por favor, verifica los archivos de datos.")
                return
        
        # Sección de Modelos Tradicionales
        if analysis_type == "Modelos Tradicionales":
            st.header("Análisis con Modelos Tradicionales")
            
            # Entrenar modelos
            with st.spinner("Entrenando modelos..."):
                results, scaler = train_models(X, y)
                if results is None:
                    st.error("Error al entrenar los modelos.")
                    return
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            for name, metrics in results.items():
                with col1:
                    st.metric(
                        f"{name} - MSE",
                        f"{metrics['mse']:.4f}"
                    )
                with col2:
                    st.metric(
                        f"{name} - R²",
                        f"{metrics['r2']:.4f}"
                    )
                with col3:
                    st.metric(
                        f"{name} - RMSE",
                        f"{np.sqrt(metrics['mse']):.4f}"
                    )
            
            # Análisis de importancia de características
            st.subheader("Importancia de Características")
            best_model = max(results.items(), key=lambda x: x[1]['r2'])[1]['model']
            fig_importance = analyze_feature_importance(best_model, X, features)
            if fig_importance:
                st.plotly_chart(fig_importance, use_container_width=True)
        
        # Sección de Análisis de Residuos
        else:
            st.header("Análisis de Residuos")
            
            try:
                # Entrenar modelo para análisis de residuos
                with st.spinner("Entrenando modelo para análisis de residuos..."):
                    results, scaler = train_models(X, y)
                    if results is None:
                        st.error("Error al entrenar el modelo.")
                        return
                    
                    # Obtener el mejor modelo
                    best_model = max(results.items(), key=lambda x: x[1]['r2'])[1]['model']
                    
                    # Dividir datos para análisis de residuos
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    X_test_scaled = scaler.transform(X_test)
                    
                    # Realizar predicciones
                    y_pred = best_model.predict(X_test_scaled)
                    
                    # Mostrar métricas del modelo
                    st.subheader("Métricas del Modelo")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("MSE", f"{mean_squared_error(y_test, y_pred):.4f}")
                    with col2:
                        st.metric("R²", f"{r2_score(y_test, y_pred):.4f}")
                    
                    # Gráfico de predicciones vs valores reales
                    st.subheader("Predicciones vs Valores Reales")
                    fig_pred = plot_prediction_vs_actual(y_test, y_pred)
                    if fig_pred:
                        st.plotly_chart(fig_pred, use_container_width=True)
                    else:
                        st.warning("No se pudo generar el gráfico de predicciones vs valores reales.")
                    
                    # Gráfico de residuos
                    st.subheader("Análisis de Residuos")
                    fig_res = plot_residuals(y_test, y_pred)
                    if fig_res:
                        st.plotly_chart(fig_res, use_container_width=True)
                    else:
                        st.warning("No se pudo generar el gráfico de residuos.")
                    
                    # Análisis estadístico de residuos
                    st.subheader("Análisis Estadístico de Residuos")
                    residuals = y_test - y_pred
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Media de Residuos", f"{residuals.mean():.4f}")
                    with col2:
                        st.metric("Desviación Estándar", f"{residuals.std():.4f}")
                    with col3:
                        st.metric("Máximo Residuo", f"{residuals.max():.4f}")
                    
                    # Histograma de residuos
                    st.subheader("Distribución de Residuos")
                    fig_hist = px.histogram(
                        x=residuals,
                        title="Histograma de Residuos",
                        labels={"x": "Residuo", "y": "Frecuencia"}
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error en el análisis de residuos: {str(e)}")
                st.error(f"Tipo de error: {str(e.__class__.__name__)}")
                logger.error(f"Error en análisis de residuos: {str(e)}")
                return
        
        # Sección de Predicciones
        st.header("Realizar Predicciones")
        
        # Cargar modelo y scaler
        try:
            model = joblib.load(MODEL_DIR / 'best_model.joblib')
            scaler = joblib.load(MODEL_DIR / 'scaler.joblib')
            
            # Formulario de predicción
            with st.form("prediction_form"):
                st.subheader("Ingrese los datos para la predicción")
                
                # Crear columnas para los inputs
                cols = st.columns(3)
                inputs = {}
                
                for i, feature in enumerate(features):
                    with cols[i % 3]:
                        inputs[feature] = st.number_input(
                            f"{feature}",
                            min_value=0.0,
                            value=0.0
                        )
                
                submitted = st.form_submit_button("Predecir")
                
                if submitted:
                    # Preparar datos para predicción
                    X_pred = pd.DataFrame([inputs])
                    X_pred_scaled = scaler.transform(X_pred)
                    
                    # Realizar predicción
                    prediction = model.predict(X_pred_scaled)[0]
                    
                    # Mostrar resultado
                    st.success(f"Velocidad media predicha: {prediction:.2f} Mbps")
        
        except Exception as e:
            st.warning("El modelo de predicción no está disponible en este momento.")
            logger.error(f"Error al cargar modelo: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error en el dashboard: {str(e)}")
        st.error("Ha ocurrido un error en el dashboard. Por favor, intente nuevamente más tarde.")

if __name__ == "__main__":
    main()