import streamlit as st
from ml_analysis import (
    load_and_prepare_data,
    train_models,
    optimize_hyperparameters,
    analyze_feature_importance,
    create_neural_network,
    plot_training_history
)

st.set_page_config(layout='wide')
st.title('Análisis de Machine Learning - Conectividad ENACOM')

# Cargar y preparar datos
st.header('1. Preparación de Datos')
X, y, tecnologias = load_and_prepare_data()

# Mostrar información básica de los datos
st.subheader('Información de los Datos')
col1, col2 = st.columns(2)
with col1:
    st.write('Características (Features):')
    st.write(X.head())
with col2:
    st.write('Variable objetivo (Target):')
    st.write(y.head())

# Entrenar modelos
st.header('2. Entrenamiento de Modelos')
results, scaler = train_models(X, y)

# Mostrar resultados de los modelos
st.subheader('Resultados de los Modelos')
for model_name, model_results in results.items():
    st.write(f'**{model_name}:**')
    st.write(f'MSE: {model_results["mse"]:.4f}')
    st.write(f'R²: {model_results["r2"]:.4f}')

# Optimización de hiperparámetros
st.header('3. Optimización de Hiperparámetros')
best_params = optimize_hyperparameters(X, y)
st.write('Mejores hiperparámetros encontrados:')
st.write(best_params)

# Análisis de importancia de características
st.header('4. Análisis de Importancia de Características')
best_model = results['XGBoost']['model']
feature_importance_fig = analyze_feature_importance(best_model, X, X.columns)
st.plotly_chart(feature_importance_fig)

# Red Neuronal
st.header('5. Red Neuronal')
model, history, nn_scaler = create_neural_network(X, y)
training_history_fig = plot_training_history(history)
st.plotly_chart(training_history_fig)

# Predicciones
st.header('6. Predicciones')
st.subheader('Ingrese los valores para predecir la penetración de internet:')
col1, col2 = st.columns(2)

with col1:
    st.write('Características de Tecnología (0 o 1):')
    tech_inputs = {}
    for tech in tecnologias:
        tech_inputs[tech] = st.number_input(tech, min_value=0, max_value=1, value=0)

with col2:
    st.write('Características Demográficas:')
    poblacion = st.number_input('Población', min_value=0, value=100000)

if st.button('Realizar Predicción'):
    # Preparar datos para predicción
    input_data = pd.DataFrame([{**tech_inputs, 'Población': poblacion}])
    
    # Escalar datos
    input_scaled = scaler.transform(input_data)
    
    # Realizar predicciones con diferentes modelos
    st.subheader('Predicciones:')
    
    # Random Forest
    rf_pred = results['Random Forest']['model'].predict(input_scaled)[0]
    st.write(f'Random Forest: {rf_pred:.2f} accesos por cada 100 hogares')
    
    # XGBoost
    xgb_pred = results['XGBoost']['model'].predict(input_scaled)[0]
    st.write(f'XGBoost: {xgb_pred:.2f} accesos por cada 100 hogares')
    
    # LightGBM
    lgb_pred = results['LightGBM']['model'].predict(input_scaled)[0]
    st.write(f'LightGBM: {lgb_pred:.2f} accesos por cada 100 hogares')
    
    # Red Neuronal
    nn_input_scaled = nn_scaler.transform(input_data)
    nn_pred = model.predict(nn_input_scaled)[0][0]
    st.write(f'Red Neuronal: {nn_pred:.2f} accesos por cada 100 hogares') 