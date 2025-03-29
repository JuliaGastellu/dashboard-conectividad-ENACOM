import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score
import shap
import optuna
import joblib
import tensorflow as tf
from tensorflow import keras
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def load_and_prepare_data():
    """Carga y prepara los datos para el análisis de ML"""
    mapa_conectividad = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/mapa_conectividad.csv')
    penetracion_hogares = pd.read_csv('https://raw.githubusercontent.com/JuliaGastellu/dashboard-conectividad-ENACOM/JuliaGastellu/data/Penetracion-hogares.csv')
    
    # Preparar features para el modelo
    tecnologias = ['ADSL', 'Cablemódem', 'Dial Up', 'Fibra óptica', 'Satelital', 'Wireless', 'Telefonía Fija', '3G', '4G']
    
    # Crear features numéricos
    X = mapa_conectividad[tecnologias + ['Población']].copy()
    y = penetracion_hogares.groupby('Provincia')['Accesos por cada 100 hogares'].mean()
    
    return X, y, tecnologias

def train_models(X, y):
    """Entrena diferentes modelos de ML"""
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Escalar features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelos
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(random_state=42),
        'LightGBM': lgb.LGBMRegressor(random_state=42)
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
    
    return results, scaler

def optimize_hyperparameters(X, y):
    """Optimiza hiperparámetros usando Optuna"""
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_float('subsample', 0.6, 0.9)
        }
        
        model = xgb.XGBRegressor(**params, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return mean_squared_error(y_test, y_pred)
    
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=50)
    
    return study.best_params

def analyze_feature_importance(model, X, feature_names):
    """Analiza la importancia de las características usando SHAP"""
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Crear gráfico de importancia
    fig = go.Figure()
    importance = np.abs(shap_values).mean(0)
    sorted_idx = np.argsort(importance)
    
    fig.add_trace(go.Bar(
        x=importance[sorted_idx],
        y=[feature_names[i] for i in sorted_idx],
        orientation='h'
    ))
    
    fig.update_layout(
        title='Importancia de Características (SHAP)',
        xaxis_title='Importancia',
        yaxis_title='Característica'
    )
    
    return fig

def create_neural_network(X, y):
    """Crea y entrena una red neuronal"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Escalar datos
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Crear modelo
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    
    # Entrenar modelo
    history = model.fit(
        X_train_scaled, y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        verbose=0
    )
    
    return model, history, scaler

def plot_training_history(history):
    """Visualiza el historial de entrenamiento de la red neuronal"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=history.history['loss'],
        name='Pérdida de Entrenamiento'
    ))
    
    fig.add_trace(go.Scatter(
        y=history.history['val_loss'],
        name='Pérdida de Validación'
    ))
    
    fig.update_layout(
        title='Historial de Entrenamiento',
        xaxis_title='Época',
        yaxis_title='Pérdida'
    )
    
    return fig 