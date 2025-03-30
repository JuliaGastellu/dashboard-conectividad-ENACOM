import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV
import joblib
import logging
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Definir directorios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'
MODEL_DIR.mkdir(exist_ok=True)

def load_data():
    """Cargar y preparar datos para el modelo."""
    try:
        # Cargar datasets
        velocidad = pd.read_parquet(DATA_DIR / 'Internet_Velocidad_Media_de_Descarga_Provincias.parquet')
        penetracion = pd.read_parquet(DATA_DIR / 'Internet_Penetración_Provincias.parquet')
        tecnologia = pd.read_parquet(DATA_DIR / 'Internet_Accesos_Tecnologia_Provincias.parquet')
        ingresos = pd.read_parquet(DATA_DIR / 'Internet_Ingresos.parquet')
        
        # Crear columna de fecha para todos los datasets
        for df in [velocidad, penetracion, tecnologia, ingresos]:
            df['fecha'] = pd.to_datetime(
                df['año'].astype(str) + '-' + 
                (df['trimestre'] * 3).astype(str).str.zfill(2) + '-01'
            )
        
        # Limpiar valores numéricos
        velocidad['mbps_(media_de_bajada)'] = velocidad['mbps_(media_de_bajada)'].str.replace(',', '.').astype(float)
        penetracion['accesos_cada_100_habitantes'] = penetracion['accesos_cada_100_habitantes'].str.replace(',', '.').astype(float)
        
        # Merge de datasets
        df = velocidad.merge(
            penetracion,
            left_on=['fecha', 'provincia'],
            right_on=['fecha', 'provincias'],
            how='inner'
        )
        
        df = df.merge(
            tecnologia,
            left_on=['fecha', 'provincia'],
            right_on=['fecha', 'provincias'],
            how='inner'
        )
        
        # Agregar características temporales
        df['mes'] = df['fecha'].dt.month
        df['trimestre'] = df['fecha'].dt.quarter
        df['año'] = df['fecha'].dt.year
        
        # Seleccionar características para el modelo
        features = [
            'accesos_cada_100_habitantes',
            'adsl',
            'cablemodem',
            'fibra_optica',
            'wireless',
            'otros',
            'mes',
            'trimestre',
            'año'
        ]
        
        target = 'mbps_(media_de_bajada)'
        
        return df, features, target
        
    except Exception as e:
        logger.error(f"Error al cargar datos: {str(e)}")
        raise

def train_model(df, features, target):
    """Entrenar y evaluar el modelo."""
    try:
        # Preparar datos
        X = df[features]
        y = df[target]
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Escalar características
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Definir modelos
        models = {
            'Random Forest': RandomForestRegressor(random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42)
        }
        
        # Entrenar y evaluar modelos
        best_model = None
        best_score = float('-inf')
        results = {}
        
        for name, model in models.items():
            # Entrenar modelo
            model.fit(X_train_scaled, y_train)
            
            # Evaluar modelo
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            
            results[name] = {
                'RMSE': rmse,
                'R2': r2,
                'MAE': mae,
                'CV Mean': cv_scores.mean(),
                'CV Std': cv_scores.std()
            }
            
            if r2 > best_score:
                best_score = r2
                best_model = model
        
        # Guardar mejor modelo y scaler
        joblib.dump(best_model, MODEL_DIR / 'best_model.joblib')
        joblib.dump(scaler, MODEL_DIR / 'scaler.joblib')
        
        return results, best_model, scaler
        
    except Exception as e:
        logger.error(f"Error al entrenar modelo: {str(e)}")
        raise

def plot_feature_importance(model, features):
    """Visualizar importancia de características."""
    try:
        importance = model.feature_importances_
        df_importance = pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        fig = px.bar(
            df_importance,
            x='importance',
            y='feature',
            title='Importancia de Características',
            orientation='h'
        )
        
        fig.write_html(MODEL_DIR / 'feature_importance.html')
        
    except Exception as e:
        logger.error(f"Error al crear gráfico de importancia: {str(e)}")
        raise

def main():
    """Función principal."""
    try:
        # Cargar datos
        logger.info("Cargando datos...")
        df, features, target = load_data()
        
        # Entrenar modelo
        logger.info("Entrenando modelo...")
        results, best_model, scaler = train_model(df, features, target)
        
        # Imprimir resultados
        logger.info("\nResultados del modelo:")
        for model_name, metrics in results.items():
            logger.info(f"\n{model_name}:")
            for metric, value in metrics.items():
                logger.info(f"{metric}: {value:.4f}")
        
        # Visualizar importancia de características
        logger.info("\nGenerando visualización de importancia de características...")
        plot_feature_importance(best_model, features)
        
        logger.info("Proceso completado exitosamente.")
        
    except Exception as e:
        logger.error(f"Error en el proceso principal: {str(e)}")
        raise

if __name__ == "__main__":
    main() 