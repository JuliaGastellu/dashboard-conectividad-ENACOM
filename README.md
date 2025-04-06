# Dashboard de Conectividad ENACOM

## 🚀 Dashboards en Línea

### Dashboard Principal
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboard-enacom.streamlit.app/)
Explora el dashboard principal con visualizaciones interactivas de la conectividad en Argentina.

### Dashboard de Machine Learning
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ml-dashboard-enacom.streamlit.app/)
Descubre las predicciones y análisis avanzados de conectividad.

---

Este proyecto analiza y visualiza datos de conectividad a internet en Argentina, utilizando datos proporcionados por ENACOM (Ente Nacional de Comunicaciones).

## Estructura del Proyecto

### 1. ETL (Extract, Transform, Load)
- **notebooks/ETL.ipynb**: Notebook que contiene el proceso de extracción, transformación y carga de datos. Realiza las siguientes tareas:
  - Carga los datos brutos de ENACOM
  - Limpia y transforma los datos
  - Crea datasets procesados en formato parquet
  - Genera datasets específicos para análisis de velocidad, penetración y tecnología

### 2. Análisis Exploratorio de Datos (EDA)
- **notebooks/EDA.ipynb**: Notebook que realiza el análisis exploratorio de los datos. Incluye:
  - Visualizaciones de tendencias temporales
  - Análisis de distribución de velocidades
  - Correlaciones entre variables
  - Estadísticas descriptivas
  - Identificación de patrones y outliers

### 3. Análisis de Machine Learning
- **ml_analysis.py**: Script que realiza el análisis de machine learning. Contiene:
  - Preparación de datos para modelado
  - Evaluación de diferentes algoritmos
  - Optimización de hiperparámetros
  - Generación de métricas de rendimiento
  - Visualización de resultados

### 4. Modelo de Velocidad
- **modelo_velocidad.py**: Script que implementa el modelo predictivo de velocidad de internet. Incluye:
  - Carga y preparación de datos
  - Entrenamiento del modelo
  - Evaluación del rendimiento
  - Guardado del modelo y scaler
  - Visualización de importancia de características

### 5. Dashboards
- **ml_dashboard.py**: Dashboard interactivo que muestra:
  - Predicciones de velocidad
  - Análisis de tendencias
  - Visualizaciones de datos
  - Simulador de velocidad
  - Métricas de rendimiento del modelo

- **dashboard.py**: Dashboard principal que muestra:
  - KPIs de conectividad
  - Evolución temporal de métricas
  - Distribución por provincia
  - Análisis de tecnología
  - Comparativas y tendencias

## Requisitos
Los requisitos del proyecto están especificados en `requirements.txt`. Las principales dependencias incluyen:
- streamlit==1.32.0
- pandas==2.2.0
- numpy==1.26.3
- plotly==5.18.0
- scikit-learn==1.4.0
- joblib==1.3.2
- pyarrow==15.0.0
- matplotlib==3.8.3
- seaborn==0.13.2

## Estructura de Directorios
```
dashboard-conectividad-ENACOM/
├── data/                    # Datos procesados
├── models/                  # Modelos entrenados
├── notebooks/              # Notebooks de análisis
│   ├── ETL.ipynb
│   └── EDA.ipynb
├── .gitignore              # Archivo de exclusión de Git
├── README.md               # Documentación
├── dashboard.py            # Dashboard principal
├── ml_analysis.py          # Análisis de machine learning
├── ml_dashboard.py         # Dashboard de machine learning
├── modelo_velocidad.py     # Modelo predictivo
└── requirements.txt        # Dependencias
```

## Cómo Ejecutar
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el dashboard principal:
```bash
streamlit run dashboard.py
```

3. Ejecutar el dashboard de ML:
```bash
streamlit run ml_dashboard.py
```

## Notas Adicionales
- Los datos se actualizan trimestralmente
- El modelo de velocidad se reentrena automáticamente con nuevos datos
- Los dashboards incluyen funcionalidades interactivas para análisis detallado

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




