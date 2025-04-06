import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
import os

# Definir directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

# Crear directorio models si no existe
os.makedirs(MODEL_DIR, exist_ok=True)

def load_and_prepare_data():
    """Carga y prepara los datos para el análisis de ML"""
    try:
        # Cargar datasets locales
        velocidad = pd.read_parquet(DATA_DIR / 'Internet Velocidad Media de Descarga Provincias.parquet')
        penetracion = pd.read_parquet(DATA_DIR / 'Internet Penetración Provincias.parquet')
        tecnologia = pd.read_parquet(DATA_DIR / 'Internet Accesos Tecnologia Provincias.parquet')
        
        # Imprimir estructura de los datos
        st.write("Estructura de los datos de velocidad:")
        st.write(velocidad.head())
        st.write("Columnas disponibles en velocidad:", velocidad.columns.tolist())
        
        st.write("\nEstructura de los datos de penetración:")
        st.write(penetracion.head())
        st.write("Columnas disponibles en penetración:", penetracion.columns.tolist())
        
        st.write("\nEstructura de los datos de tecnología:")
        st.write(tecnologia.head())
        st.write("Columnas disponibles en tecnología:", tecnologia.columns.tolist())
        
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
        
        # Seleccionar características
        features = [
            'accesos_cada_100_habitantes',
            'adsl',
            'cablemodem',
            'fibra_optica',
            'wireless',
            'otros'
        ]
        
        X = df[features]
        y = df['mbps_(media_de_bajada)']
        
        return X, y, features
        
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        st.error(f"Detalles del error: {str(e.__class__.__name__)}")
        return None, None, None

def train_models(X, y):
    """Entrena diferentes modelos de ML"""
    try:
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Escalar features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Entrenar modelos
        models = {
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42)
        }
        
        results = {}
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            results[name] = {
                'model': model,
                'mse': mean_squared_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred)
            }
        
        # Guardar el mejor modelo y scaler
        best_model = max(results.items(), key=lambda x: x[1]['r2'])[1]['model']
        joblib.dump(best_model, MODEL_DIR / 'best_model.joblib')
        joblib.dump(scaler, MODEL_DIR / 'scaler.joblib')
        
        return results, scaler
    except Exception as e:
        st.error(f"Error al entrenar modelos: {str(e)}")
        st.error(f"Detalles del error: {str(e.__class__.__name__)}")
        return None, None

def analyze_feature_importance(model, X, feature_names):
    """Analiza la importancia de las características"""
    try:
        importance = model.feature_importances_
        df_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        fig = px.bar(
            df_importance,
            x='importance',
            y='feature',
            title='Importancia de Características',
            orientation='h'
        )
        
        fig.update_layout(
            title='Importancia de Características',
            xaxis_title='Importancia',
            yaxis_title='Característica'
        )
        
        return fig
    except Exception as e:
        st.error(f"Error al analizar importancia de características: {str(e)}")
        return None

def plot_prediction_vs_actual(y_test, y_pred):
    """Visualiza predicciones vs valores reales"""
    try:
        fig = go.Figure()
        
        # Agregar línea de referencia
        fig.add_trace(go.Scatter(
            x=[min(y_test), max(y_test)],
            y=[min(y_test), max(y_test)],
            mode='lines',
            name='Línea de referencia',
            line=dict(color='red', dash='dash')
        ))
        
        # Agregar predicciones
        fig.add_trace(go.Scatter(
            x=y_test,
            y=y_pred,
            mode='markers',
            name='Predicciones',
            marker=dict(color='blue')
        ))
        
        fig.update_layout(
            title='Predicciones vs Valores Reales',
            xaxis_title='Valor Real',
            yaxis_title='Predicción',
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"Error al crear gráfico de predicciones: {str(e)}")
        return None

def plot_residuals(y_test, y_pred):
    """Visualiza residuos"""
    try:
        residuals = y_test - y_pred
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=y_pred,
            y=residuals,
            mode='markers',
            name='Residuos',
            marker=dict(color='blue')
        ))
        
        # Agregar línea horizontal en y=0
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig.update_layout(
            title='Análisis de Residuos',
            xaxis_title='Predicción',
            yaxis_title='Residuo',
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"Error al graficar residuos: {str(e)}")
        return None