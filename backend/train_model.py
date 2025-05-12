# backend/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # ou LightGBM
import joblib
import os
import shap

# Charger les données
data_path = os.path.join(os.path.dirname(__file__), "data.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Le fichier {data_path} est introuvable. Assurez-vous de l'avoir généré.")

df = pd.read_csv(data_path)

# Exemple : colonne cible simulée (attention à adapter selon ton projet)
# Crée une cible fictive aléatoire pour test
import numpy as np
df["TARGET"] = np.random.randint(0, 2, size=len(df))

# Séparer les features et la target
X = df.drop(columns=["SK_ID_CURR", "TARGET"])

# Remplir les NaN pour éviter les erreurs
X.fillna("missing", inplace=True)

# Encoder les variables catégorielles
X = pd.get_dummies(X)

# Adapter y
y = df["TARGET"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle ET les colonnes utilisées
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump((model, X.columns.tolist()), model_path)
print(f"✅ Modèle et colonnes sauvegardés dans {model_path}")

# Créer un explainer SHAP (TreeExplainer est adapté aux forêts aléatoires)
explainer = shap.TreeExplainer(model)

# Calculer les valeurs SHAP pour le dataset complet
shap_values = explainer.shap_values(X_train)

# Sauvegarder l’explainer et les données d’entraînement (pour l’interprétation)
explainer_path = os.path.join(os.path.dirname(__file__), "explainer.pkl")
joblib.dump((explainer, X_train), explainer_path)
print(f"✅ Explainer SHAP et données sauvegardés dans {explainer_path}")