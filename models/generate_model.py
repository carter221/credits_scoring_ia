import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Liste des features utilisées par le modèle
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

# Créer un jeu de données d'entraînement plus complet
np.random.seed(42)
n_samples = 100

# Créer des exemples non-défaut (classe 0)
X_no_default = []
for _ in range(n_samples // 2):
    sample = [
        np.random.randint(0, 2),                # CNT_CHILDREN
        np.random.uniform(100000, 220000),      # AMT_CREDIT
        np.random.uniform(90000, 200000),       # AMT_GOODS_PRICE
        np.random.randint(-7000, -2000),        # DAYS_EMPLOYED
        1,                                      # FLAG_EMP_PHONE
        np.random.randint(1, 3),                # CNT_FAM_MEMBERS
        1,                                      # REGION_RATING_CLIENT
        1,                                      # REGION_RATING_CLIENT_W_CITY
        0,                                      # REG_REGION_NOT_WORK_REGION
        0,                                      # LIVE_REGION_NOT_WORK_REGION
        0,                                      # REG_CITY_NOT_WORK_CITY
        0,                                      # LIVE_CITY_NOT_WORK_CITY
        np.random.uniform(0.8, 1.0),            # YEARS_BEGINEXPLUATATION_AVG
        np.random.uniform(0.8, 1.0),            # FLOORSMAX_AVG
        np.random.uniform(0.8, 1.0),            # YEARS_BEGINEXPLUATATION_MODE
        np.random.uniform(0.8, 1.0),            # FLOORSMAX_MODE
        np.random.uniform(0.8, 1.0),            # YEARS_BEGINEXPLUATATION_MEDI
        np.random.uniform(0.8, 1.0),            # FLOORSMAX_MEDI
        0,                                      # OBS_30_CNT_SOCIAL_CIRCLE
        0,                                      # DEF_30_CNT_SOCIAL_CIRCLE
        0,                                      # OBS_60_CNT_SOCIAL_CIRCLE
        0                                       # DEF_60_CNT_SOCIAL_CIRCLE
    ]
    X_no_default.append(sample)

# Créer des exemples défaut (classe 1)
X_default = []
for _ in range(n_samples // 2):
    sample = [
        np.random.randint(2, 4),                # CNT_CHILDREN
        np.random.uniform(250000, 400000),      # AMT_CREDIT
        np.random.uniform(225000, 350000),      # AMT_GOODS_PRICE
        np.random.randint(-2000, -500),         # DAYS_EMPLOYED
        0,                                      # FLAG_EMP_PHONE
        np.random.randint(4, 6),                # CNT_FAM_MEMBERS
        np.random.randint(2, 3),                # REGION_RATING_CLIENT
        np.random.randint(2, 3),                # REGION_RATING_CLIENT_W_CITY
        1,                                      # REG_REGION_NOT_WORK_REGION
        1,                                      # LIVE_REGION_NOT_WORK_REGION
        1,                                      # REG_CITY_NOT_WORK_CITY
        1,                                      # LIVE_CITY_NOT_WORK_CITY
        np.random.uniform(0.5, 0.7),            # YEARS_BEGINEXPLUATATION_AVG
        np.random.uniform(0.5, 0.7),            # FLOORSMAX_AVG
        np.random.uniform(0.5, 0.7),            # YEARS_BEGINEXPLUATATION_MODE
        np.random.uniform(0.5, 0.7),            # FLOORSMAX_MODE
        np.random.uniform(0.5, 0.7),            # YEARS_BEGINEXPLUATATION_MEDI
        np.random.uniform(0.5, 0.7),            # FLOORSMAX_MEDI
        np.random.randint(1, 3),                # OBS_30_CNT_SOCIAL_CIRCLE
        np.random.randint(1, 3),                # DEF_30_CNT_SOCIAL_CIRCLE
        np.random.randint(1, 3),                # OBS_60_CNT_SOCIAL_CIRCLE
        np.random.randint(1, 3)                 # DEF_60_CNT_SOCIAL_CIRCLE
    ]
    X_default.append(sample)

# Combiner les données
X = np.vstack([X_no_default, X_default])
y = np.hstack([np.zeros(n_samples // 2), np.ones(n_samples // 2)])

# Créer et entraîner le modèle
print("Entraînement du modèle Random Forest...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)
model.fit(X, y)

# Tester quelques prédictions
test_samples = [X[0], X[n_samples // 2]]
for i, sample in enumerate(test_samples):
    proba = model.predict_proba([sample])[0][1]
    pred = model.predict([sample])[0]
    print(f"Échantillon {i+1}: prédiction={pred}, probabilité={proba:.4f}")

# Sauvegarder le modèle
output_path = "random_forest_model.pkl"
with open(output_path, "wb") as f:
    pickle.dump(model, f)

print(f"Modèle sauvegardé sous: {output_path}")
