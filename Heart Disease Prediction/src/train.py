import joblib
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Load preprocessed data
scaler = joblib.load("models/scaler.pkl")
X_train, X_test, y_train, y_test = joblib.load("models/data.pkl")

# Optimized XGBoost Model
xgb_model = XGBClassifier(
    n_estimators=250, max_depth=5, learning_rate=0.03, 
    reg_lambda=3, reg_alpha=2, min_child_weight=3, random_state=42
)
xgb_model.fit(X_train, y_train)

# Optimized RandomForest Model
rf_model = RandomForestClassifier(
    n_estimators=150, max_depth=8, min_samples_split=10, 
    min_samples_leaf=5, class_weight="balanced", random_state=42
)
rf_model.fit(X_train, y_train)

# Save models
joblib.dump(xgb_model, "models/best_xgb_model.pkl")
joblib.dump(rf_model, "models/best_rf_model.pkl")

print("✅ Models trained with improved generalization!")
