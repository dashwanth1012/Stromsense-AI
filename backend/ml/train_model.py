import pandas as pd

from sklearn.ensemble import RandomForestClassifier

import joblib

# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("weather_training.csv")

# ==========================================
# FEATURES
# ==========================================

X = data[
    [
        "cape",
        "lifted_index",
        "sweat_index",
        "k_index",
        "pwat"
    ]
]

# ==========================================
# TARGET
# ==========================================

y = data["storm"]

# ==========================================
# TRAIN MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "storm_model.pkl"
)

print("✅ MODEL TRAINED SUCCESSFULLY")