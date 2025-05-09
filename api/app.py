import os
import json
import numpy as np
import pandas as pd
import h5py
import tempfile
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import lightgbm as lgb
from xgboost import XGBClassifier
import tensorflow as tf
from sklearn.impute import SimpleImputer  # Utilisation de SimpleImputer à la place d'Imputer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Définir les chemins des fichiers modèle et préprocesseurs
MODEL_PATH = '../models/'
model_file = os.path.join(MODEL_PATH, 'lightgbm.h5')  # Remplacez par le nom de votre meilleur modèle
metadata_file = os.path.join(MODEL_PATH, 'lightgbm_metadata.h5')  # Fichier de métadonnées correspondant
preprocessing_file = os.path.join(MODEL_PATH, 'preprocessing.h5')

# Fonction pour charger un modèle h5 selon son type
def load_model_from_h5(file_path, metadata_path):
    """
    Charge un modèle à partir d'un fichier h5
    """
    # D'abord, déterminer le type de modèle à partir des métadonnées
    with h5py.File(metadata_path, 'r') as h5file:
        model_type = h5file.attrs['model_type']
    
    if model_type == 'LGBMClassifier':  # LightGBM models
        model = lgb.Booster(model_file=file_path)
        # Convertir le booster en LGBMClassifier
        classifier = lgb.LGBMClassifier()
        classifier._Booster = model
        return classifier
        
    elif model_type == 'XGBClassifier':  # XGBoost models
        model = XGBClassifier()
        model.load_model(file_path)
        return model
        
    else:  # Scikit-learn models (RandomForest, LogisticRegression, etc.)
        # Charger le modèle depuis le format h5
        with h5py.File(file_path, 'r') as h5file:
            sklearn_group = h5file['sklearn_model']
            model_dump = sklearn_group['model_dump'][()]
            
            # Écrire le dump dans un fichier temporaire
            temp_file = tempfile.NamedTemporaryFile(delete=False).name
            with open(temp_file, 'wb') as f:
                f.write(model_dump.tobytes())
                
            # Charger le modèle depuis le fichier temporaire
            with open(temp_file, 'rb') as f:
                model = pickle.load(f)
                
            # Supprimer le fichier temporaire
            os.remove(temp_file)
            
        return model

# Fonction pour charger les préprocesseurs
def load_preprocessors(file_path):
    with h5py.File(file_path, 'r') as h5file:
        # Charger l'imputer
        imputer_group = h5file['imputer']
        imputer_data = imputer_group['data'][()]
        
        # Charger le scaler
        scaler_group = h5file['scaler']
        scaler_data = scaler_group['data'][()]
        
        # Écrire les dumps dans des fichiers temporaires
        imputer_temp = tempfile.NamedTemporaryFile(delete=False).name
        scaler_temp = tempfile.NamedTemporaryFile(delete=False).name
        
        with open(imputer_temp, 'wb') as f:
            f.write(imputer_data.tobytes())
        
        with open(scaler_temp, 'wb') as f:
            f.write(scaler_data.tobytes())
        
        # Charger les objets depuis les fichiers temporaires
        with open(imputer_temp, 'rb') as f:
            imputer = pickle.load(f)
        
        with open(scaler_temp, 'rb') as f:
            scaler = pickle.load(f)
        
        # Supprimer les fichiers temporaires
        os.remove(imputer_temp)
        os.remove(scaler_temp)
        
    return imputer, scaler

# Charger le modèle et les préprocesseurs au démarrage de l'application
print("Chargement du modèle et des préprocesseurs...")
try:
    model = load_model_from_h5(model_file, metadata_file)
    imputer, scaler = load_preprocessors(preprocessing_file)
    
    # Charger les noms des caractéristiques
    with h5py.File(metadata_file, 'r') as h5file:
        feature_group = h5file['features']
        features = [feature_group.attrs[f'feature_{i}'] for i in range(len(feature_group.attrs))]
    
    print(f"Modèle {type(model).__name__} chargé avec succès!")
    print(f"Caractéristiques: {features}")

    MODEL_LOADED = True
except Exception as e:
    print(f"Erreur lors du chargement du modèle ou des préprocesseurs: {e}")
    MODEL_LOADED = False

@app.route('/')
def home():
    return "API de Scoring Crédit Home Credit - Status: " + ("En ligne" if MODEL_LOADED else "Erreur de chargement du modèle")

@app.route('/predict', methods=['POST'])
def predict():
    if not MODEL_LOADED:
        return jsonify({
            'error': 'Le modèle n\'a pas été chargé correctement.'
        }), 500

    try:
        # Récupérer les données du client
        client_data = request.json
        
        # Vérifier si les données requises sont présentes
        required_fields = features  # Utiliser les noms de caractéristiques chargés depuis le modèle
        
        # Créer un DataFrame avec les caractéristiques
        data = pd.DataFrame([client_data], columns=features)
        
        # Prétraiter les données
        data = data.replace([np.inf, -np.inf], np.nan)  # Remplacer les valeurs infinies
        data_imputed = imputer.transform(data)
        data_scaled = scaler.transform(data_imputed)
        
        # Faire la prédiction
        probability = model.predict_proba(data_scaled)[0, 1]
        prediction = 1 if probability > 0.5 else 0
        
        # Calculer l'importance des caractéristiques
        # Note: cela peut varier selon le type de modèle
        feature_importance = {}
        if hasattr(model, 'feature_importances_'):
            for i, feature in enumerate(features):
                feature_importance[feature] = float(model.feature_importances_[i])
        else:
            # Si le modèle n'a pas d'importances de caractéristiques, utiliser des valeurs fictives
            for feature in features:
                feature_importance[feature] = 1.0 / len(features)
        
        # Normaliser les importances pour qu'elles somment à 1
        total_importance = sum(feature_importance.values())
        feature_importance = {k: v/total_importance for k, v in feature_importance.items()}
        
        return jsonify({
            'client_id': client_data.get('client_id', 'unknown'),
            'probability': float(probability),
            'prediction': int(prediction),
            'threshold': 0.5,
            'feature_importance': feature_importance
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la prédiction: {str(e)}'
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    if not MODEL_LOADED:
        return jsonify({
            'error': 'Le modèle n\'a pas été chargé correctement.'
        }), 500
    
    try:
        # Récupérer les informations du modèle
        with h5py.File(metadata_file, 'r') as h5file:
            model_type = h5file.attrs['model_type']
            auc_score = float(h5file.attrs['auc_score'])
        
        return jsonify({
            'model_type': model_type,
            'auc_score': auc_score,
            'features': features,
            'threshold': 0.5  # Seuil par défaut
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erreur lors de la récupération des informations du modèle: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
