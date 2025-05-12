import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Créer le dossier backend s'il n'existe pas
os.makedirs("backend", exist_ok=True)

n = 100

df = pd.DataFrame({
    "SK_ID_CURR": range(100001, 100001 + n),
    "CODE_GENDER": np.random.choice(["M", "F"], size=n),
    "AMT_INCOME_TOTAL": np.random.normal(150000, 50000, size=n).round(2),
    "AMT_CREDIT": np.random.normal(600000, 100000, size=n).round(2),
    "DAYS_BIRTH": -np.random.randint(25*365, 65*365, size=n),
    "DAYS_EMPLOYED": -np.random.randint(0, 40*365, size=n),
    "NAME_FAMILY_STATUS": np.random.choice(["Married", "Single", "Divorced"], size=n),
    "NAME_EDUCATION_TYPE": np.random.choice(["Higher education", "Secondary", "Incomplete"], size=n),
    "TARGET": np.random.randint(0, 2, size=n)
})

df.to_csv("backend/data.csv", index=False)
print("✅ Données générées dans backend/data.csv")