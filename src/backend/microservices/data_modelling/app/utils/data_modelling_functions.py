# Importamos librerias
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split  # Para dividir los datos
from sklearn.metrics import accuracy_score  # Para evaluar el modelo
import os  # Para manejo de rutas de archivos y directorios
import logging  # Para el registro de logs





# Inicializa el logging
logger = logging.getLogger(__name__)

# Función para entrenar un modelo de machine learning

def model_training(df, model_type, hyperparameters, file_location, target_variable, features, test_size, random_state=None):
    """
    Entrena un modelo de machine learning basado en el tipo y los hiperparámetros especificados.
    Args:
        df (pd.DataFrame): El DataFrame con los datos a entrenar.
        model_type (str): El tipo de modelo a entrenar.
        hyperparameters (dict): Un diccionario con los hiperparámetros para el modelo.
        file_location (str): La ubicación base para guardar el modelo entrenado.
    
    Returns:
        tuple: Una tupla conteniendo la ruta del archivo del modelo entrenado y un mensaje.
    """
    logger.info(f"Entrenando modelo de tipo {model_type} con hiperparámetros {hyperparameters}")

    # Dividir el dataset en variables predictoras y variable objetivo
    # Obtenemos las variables predictoras y la variable objetivo del diccionario de hiperparametros

    X = df[features]
    y = df[target_variable]

    # Dividir el dataset en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    model = None
    if model_type == "random_forest_classifier":
        model = RandomForestClassifier(**hyperparameters)
    elif model_type == "gradient_boosting":
        model = GradientBoostingClassifier(**hyperparameters)
    elif model_type == "logistic_regression":
        model = LogisticRegression(**hyperparameters)
    elif model_type == "svm":
        model = SVC(**hyperparameters)
    elif model_type == "knn":
        model = KNeighborsClassifier(**hyperparameters)
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier(**hyperparameters)
    elif model_type == "naive_bayes":
        model = GaussianNB(**hyperparameters)
    elif model_type == "mlp":
        model = MLPClassifier(**hyperparameters)
    elif model_type == "xgboost":
        model = XGBClassifier(**hyperparameters)
    elif model_type == "lightgbm":
        model = LGBMClassifier(**hyperparameters)
    elif model_type == "catboost":
        model = CatBoostClassifier(**hyperparameters)
    elif model_type == "random_forest_regressor":
        model = RandomForestRegressor(**hyperparameters)

    # Añadir aquí más modelos si es necesario
    else:
        raise ValueError("Tipo de modelo no soportado")

    # Entrenar el modelo
    model.fit(X_train, y_train)
    
    # Evaluar el modelo
    predictions = model.predict(X_test)

    # De momento evalua con accurary, pendiente de ampliar opciones
    accuracy = accuracy_score(y_test, predictions)
    
    # Guardar el modelo
    model_file_path = os.path.join(file_location, f"{model_type}_model.joblib")
    joblib.dump(model, model_file_path)
    
    message = f"Modelo {model_type} entrenado con una precisión de {accuracy:.4f}"
    return model_file_path, message
