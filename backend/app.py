# backend/app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import joblib
import shap
import numpy as np

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines par défaut

# Charger les données et le modèle
data_path = os.path.join(os.path.dirname(__file__), "data.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Le fichier {data_path} est introuvable. Assurez-vous de l'avoir généré.")

df = pd.read_csv(data_path)
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le fichier {model_path} est introuvable. Assurez-vous de l'avoir généré.")

model, model_columns = joblib.load(model_path)

@app.route("/api/client/<int:client_id>", methods=["GET"])
def get_client_data(client_id):
    client = df[df["SK_ID_CURR"] == client_id]
    if client.empty:
        return jsonify({"error": "Client not found"}), 404
    return client.to_json(orient="records")

@app.route("/api/predict/<int:client_id>", methods=["GET"])
def predict_score(client_id):
    print(f"Requête pour le score du client avec ID : {client_id}")
    client = df[df["SK_ID_CURR"] == client_id]
    if client.empty:
        print("Client non trouvé")
        return jsonify({"error": "Client non trouvé"}), 404

    features = client.drop(columns=["SK_ID_CURR", "TARGET"])
    features_encoded = pd.get_dummies(features)
    missing_cols = set(model.feature_names_in_) - set(features_encoded.columns)
    for col in missing_cols:
        features_encoded[col] = 0
    features_encoded = features_encoded[model.feature_names_in_]

    score = model.predict_proba(features_encoded)[0][1]
    print("Score brut retourné par le modèle :", score)
    return jsonify({"score": round(score * 100, 2)})

@app.route("/api/explain/<int:client_id>", methods=["GET"])
def explain(client_id):
    client_data = df[df["SK_ID_CURR"] == client_id]

    if client_data.empty:
        return jsonify({"error": "Client not found"}), 404

    # Préparer les données pour le modèle
    X = df.drop(columns=["SK_ID_CURR"])  # Ce que le modèle attend en entrée
    client_input = X.loc[client_data.index]

    # Remplir les valeurs manquantes
    client_input.fillna("missing", inplace=True)

    # Encoder les variables catégoriques
    client_input = pd.get_dummies(client_input)

    # Réaligner les colonnes comme lors de l'entraînement
    client_input = client_input.reindex(columns=model_columns, fill_value=0)

    # Vérifier que toutes les colonnes sont numériques
    if not all(client_input.dtypes.apply(lambda dtype: np.issubdtype(dtype, np.number))):
        return jsonify({"error": "Non-numeric data found in input after preprocessing"}), 500

    # Créer un explainer SHAP avec un sous-échantillon des données d'entraînement
    explainer = shap.Explainer(model.predict, X.sample(100, random_state=42))

    # Explication pour le client
    shap_values = explainer(client_input)

    # Extraire les contributions SHAP
    values = shap_values.values[0]  # car un seul client
    features = shap_values.feature_names
    input_data = client_input.iloc[0].values

    # Trier les contributions par importance absolue
    top_features = sorted(
        zip(features, input_data, values),
        key=lambda x: abs(x[2]),
        reverse=True
    )[:10]

    return jsonify({
        "top_contributions": [
            {"feature": name, "value": val, "contribution": float(contr)}
            for name, val, contr in top_features
        ]
    })

@app.route("/api/client/<int:client_id>", methods=["GET"])
def get_client_info(client_id):
    print(f"Requête pour les données du client avec ID : {client_id}")
    client = df[df["SK_ID_CURR"] == client_id]
    if client.empty:
        print("Client non trouvé")
        return jsonify({"error": "Client non trouvé"}), 404

    client_data = client.iloc[0]
    print("Données client récupérées :", client_data.to_dict())
    return jsonify({
        "id": int(client_data["SK_ID_CURR"]),
        "genre": client_data["CODE_GENDER"],
        "revenu": float(client_data["AMT_INCOME_TOTAL"]),
        "montant_credit": float(client_data["AMT_CREDIT"]),
        "statut_familial": client_data["NAME_FAMILY_STATUS"]
    })

if __name__ == "__main__":
    app.run(debug=True)