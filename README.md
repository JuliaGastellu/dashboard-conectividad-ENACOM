# Dashboard de Conectividad ENACOM con Análisis Predictivo

## Descripción
Este proyecto es una herramienta avanzada de análisis de datos y machine learning para visualizar y predecir la conectividad a internet en Argentina. Utilizando datos públicos proporcionados por ENACOM (Ente Nacional de Comunicaciones), este proyecto personal combina visualización interactiva con modelos predictivos para ofrecer una visión completa del estado actual y futuro de la conectividad en el país. El objetivo es demostrar el potencial del análisis de datos y machine learning en el contexto de la conectividad digital.

## Características Principales

### 📊 Dashboard Interactivo
- Visualización dinámica de datos de conectividad por provincia
- Filtros interactivos por año y región
- Gráficos de penetración de internet
- Análisis detallado de tecnologías disponibles
- Mapa interactivo de Argentina con datos de conectividad

### 🤖 Análisis Predictivo
- **Modelos de Machine Learning:**
  - Random Forest para predicciones robustas
  - XGBoost para análisis de alta precisión
  - LightGBM para predicciones rápidas
  - Red Neuronal para patrones complejos

- **Características Avanzadas:**
  - Optimización automática de hiperparámetros
  - Análisis de importancia de características
  - Visualización del entrenamiento de modelos
  - Interfaz interactiva para predicciones en tiempo real

## Hallazgos Principales

### Tendencias Tecnológicas y Transición Digital
- La fibra óptica domina en áreas urbanas debido a la demanda de alta velocidad
- Las tecnologías inalámbricas (4G/5G) crecen en regiones rurales
- Se observa una clara tendencia hacia tecnologías más modernas

### Disparidades Regionales y Patrones de Crecimiento
- La fibra óptica se expande rápidamente en ciudades
- Las tecnologías antiguas (ADSL, dial-up) están en declive
- Las tasas de crecimiento varían significativamente entre provincias
- Las políticas públicas influyen en el desarrollo de la conectividad

### Factores que Influyen en la Conectividad
- Ciclos económicos y su impacto en la inversión en infraestructura
- Políticas regulatorias y su efecto en la competencia
- Eventos externos (pandemias, desastres naturales)
- Gestión del espectro radioeléctrico

### Brechas Urbano-Rurales
- Las áreas urbanas muestran adopción más rápida de tecnologías
- Las regiones rurales presentan retrasos en la infraestructura
- Se observan diferencias significativas en la competencia entre proveedores

## KPIs para Medir el Progreso
- **KPI 1:** Crecimiento del Acceso a Internet – Aumentar la penetración en hogares en un 2% por provincia
- **KPI 2:** Expansión de Fibra Óptica – Incrementar la adopción en un 2% por provincia
- **KPI 3:** Conectividad de Alta Velocidad – Mejorar las conexiones superiores a 20 Mbps en un 5%

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/dashboard-conectividad-ENACOM.git
cd dashboard-conectividad-ENACOM
```

2. Crear y activar entorno virtual:
```bash
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar el dashboard:
```bash
streamlit run dashboard.py
```

## Estructura del Proyecto
```
dashboard-conectividad-ENACOM/
├── data/                   # Datos del proyecto
├── notebooks/             # Jupyter notebooks para análisis
├── images/               # Recursos visuales
├── dashboard.py          # Dashboard principal
├── ml_analysis.py        # Funciones de machine learning
├── ml_dashboard.py       # Dashboard de machine learning
└── requirements.txt      # Dependencias del proyecto
```

## Uso del Dashboard

### Dashboard Principal
1. Seleccione un año y una provincia en la barra lateral
2. Explore los diferentes gráficos y visualizaciones
3. Analice la distribución de tecnologías por provincia
4. Observe las tendencias de penetración de internet

### Sección de Machine Learning
1. Acceda a la página de ML desde el menú lateral
2. Explore los resultados de los diferentes modelos
3. Realice predicciones ingresando valores de entrada
4. Analice la importancia de las características
5. Compare el rendimiento de diferentes modelos

## Tecnologías Utilizadas
- Python 3.x
- Streamlit para la interfaz de usuario
- Pandas y NumPy para el procesamiento de datos
- Scikit-learn, XGBoost, LightGBM para machine learning
- TensorFlow para redes neuronales
- Plotly para visualizaciones interactivas
- SHAP para análisis de importancia de características

## Contribución
Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Fork el repositorio
2. Cree una rama para su feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit sus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abra un Pull Request


## Contacto
Mail: juliacgastellu@gmail.com
LinkedIn: https://www.linkedin.com/in/julia-gastellu/

Link del Proyecto: [https://github.com/tu-usuario/dashboard-conectividad-ENACOM](https://github.com/JuliaGastellu/dashboard-conectividad-ENACOM)



