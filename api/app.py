from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import h5py
import numpy as np
import sqlite3
import warnings
import joblib

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ImportWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

app = Flask(__name__)
CORS(app)

# Chemins des modèles et du scaler
MODEL_PATH = '../models/random_forest_smote_model.h5'
SCALER_PATH = '../models/standard_scaler.h5'
DB_PATH = '../db/credit_scoring_simplified.sqlite3'

# Liste ordonnée des features attendues par le modèle
MODEL_FEATURES = [
    'CNT_CHILDREN', 'AMT_CREDIT', 'AMT_GOODS_PRICE', 'DAYS_EMPLOYED',
    'FLAG_EMP_PHONE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT',
    'REGION_RATING_CLIENT_W_CITY', 'REG_REGION_NOT_WORK_REGION',
    'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_WORK_CITY',
    'LIVE_CITY_NOT_WORK_CITY', 'YEARS_BEGINEXPLUATATION_AVG',
    'FLOORSMAX_AVG', 'YEARS_BEGINEXPLUATATION_MODE', 'FLOORSMAX_MODE',
    'YEARS_BEGINEXPLUATATION_MEDI', 'FLOORSMAX_MEDI',
    'OBS_30_CNT_SOCIAL_CIRCLE', 'DEF_30_CNT_SOCIAL_CIRCLE',
    'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE'
]

def load_pickle_from_h5(h5_path, dataset):
    with h5py.File(h5_path, 'r') as h5file:
        pickled_bytes = h5file[dataset][()]
    return pickle.loads(pickled_bytes)

# Charger le modèle et le scaler
try:
    rf_model = joblib.load(MODEL_PATH)
    print(f"Modèle chargé depuis {MODEL_PATH}")
    
    # Charger le StandardScaler
    standard_scaler = joblib.load(SCALER_PATH)
    print(f"Scaler chargé depuis {SCALER_PATH}")
except Exception as e:
    print(f"Impossible de charger le modèle ou le scaler: {str(e)}")
    rf_model = None
    standard_scaler = None

def get_client_features_from_db(sk_id_curr):
    """
    Récupère les features du client depuis la base sqlite3.
    Retourne un dictionnaire {feature: valeur}
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # accès par nom de colonne
    cur = conn.cursor()
    
    # Nouvelle requête adaptée à la structure simplifiée de la base de données
    cur.execute("""
        SELECT *
        FROM clients
        WHERE sk_id_curr = ?
    """, (sk_id_curr,))
    
    row = cur.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    # Utiliser directement les champs de la table clients
    client_features = {
        'CNT_CHILDREN': row['CNT_CHILDREN'],
        'CODE_GENDER': row['CODE_GENDER'],
        'AMT_CREDIT': row['AMT_CREDIT'],
        'AMT_GOODS_PRICE': row['AMT_GOODS_PRICE'],
        'DAYS_EMPLOYED': row['DAYS_EMPLOYED'],
        'FLAG_EMP_PHONE': row['FLAG_EMP_PHONE'],
        'CNT_FAM_MEMBERS': row['CNT_FAM_MEMBERS'],
        'REGION_RATING_CLIENT': row['REGION_RATING_CLIENT'],
        'REGION_RATING_CLIENT_W_CITY': row['REGION_RATING_CLIENT_W_CITY'],
        'REG_REGION_NOT_WORK_REGION': row['REG_REGION_NOT_WORK_REGION'],
        'LIVE_REGION_NOT_WORK_REGION': row['LIVE_REGION_NOT_WORK_REGION'],
        'REG_CITY_NOT_WORK_CITY': row['REG_CITY_NOT_WORK_CITY'],
        'LIVE_CITY_NOT_WORK_CITY': row['LIVE_CITY_NOT_WORK_CITY'],
        'YEARS_BEGINEXPLUATATION_AVG': row['YEARS_BEGINEXPLUATATION_AVG'],
        'FLOORSMAX_AVG': row['FLOORSMAX_AVG'],
        'YEARS_BEGINEXPLUATATION_MODE': row['YEARS_BEGINEXPLUATATION_MODE'],
        'FLOORSMAX_MODE': row['FLOORSMAX_MODE'],
        'YEARS_BEGINEXPLUATATION_MEDI': row['YEARS_BEGINEXPLUATATION_MEDI'],
        'FLOORSMAX_MEDI': row['FLOORSMAX_MEDI'],
        'OBS_30_CNT_SOCIAL_CIRCLE': row['OBS_30_CNT_SOCIAL_CIRCLE'],
        'DEF_30_CNT_SOCIAL_CIRCLE': row['DEF_30_CNT_SOCIAL_CIRCLE'],
        'OBS_60_CNT_SOCIAL_CIRCLE': row['OBS_60_CNT_SOCIAL_CIRCLE'],
        'DEF_60_CNT_SOCIAL_CIRCLE': row['DEF_60_CNT_SOCIAL_CIRCLE']
    }
    
    return client_features

@app.route('/')
def home():
    return "API de Scoring Crédit Home Credit - Status: En ligne (mode prod)"

@app.route('/predict/<int:sk_id_curr>', methods=['GET'])
def predict(sk_id_curr):
    # 1. Chercher les infos du client dans la base
    client_features = get_client_features_from_db(sk_id_curr)
    if client_features is None:
        return jsonify({'error': f'Client {sk_id_curr} introuvable'}), 404

    # 2. Vérifier que toutes les features nécessaires sont présentes
    missing_features = [feat for feat in MODEL_FEATURES if feat not in client_features or client_features[feat] is None]
    if missing_features:
        # Remplir les valeurs manquantes avec la médiane (0 pour simplicité ici)
        for feat in missing_features:
            client_features[feat] = 0
        print(f"Warning: Features manquantes remplies avec 0: {missing_features}")

    # 3. Préparer les features pour le modèle (attention à l'ordre !)
    try:
        # Créer un array numpy avec les features dans le bon ordre
        features = np.array([client_features[feat] for feat in MODEL_FEATURES]).reshape(1, -1)
        
        # Standardiser les données si le scaler est disponible
        if standard_scaler is not None:
            features = standard_scaler.transform(features)
            print("Données standardisées avec le scaler")
        
        # 4. Prédiction avec le modèle
        proba = rf_model.predict_proba(features)[0, 1]
        prediction = int(rf_model.predict(features)[0])
        
        # 5. Retourner la prédiction et la proba
        return jsonify({
            'sk_id_curr': sk_id_curr,
            'prediction': prediction,
            'proba': float(proba),
            'client_info': {
                'gender': client_features.get('CODE_GENDER', 'Unknown'),
                'credit_amount': float(client_features.get('AMT_CREDIT', 0)),
                'goods_price': float(client_features.get('AMT_GOODS_PRICE', 0)),
                'employment_years': abs(int(client_features.get('DAYS_EMPLOYED', 0))) // 365,
                'family_members': float(client_features.get('CNT_FAM_MEMBERS', 0)),
                'children_count': int(client_features.get('CNT_CHILDREN', 0)),
                'region_rating': int(client_features.get('REGION_RATING_CLIENT', 0))
            },
            'model_features': {feat: float(client_features.get(feat, 0)) for feat in MODEL_FEATURES}
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erreur lors de la prédiction: {str(e)}\n{error_details}")
        return jsonify({
            'error': f'Erreur lors de la prédiction: {str(e)}',
            'details': str(error_details)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)