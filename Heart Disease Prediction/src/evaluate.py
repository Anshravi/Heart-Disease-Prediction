import joblib
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

# Load models and data
xgb_model = joblib.load("models/best_xgb_model.pkl")
rf_model = joblib.load("models/best_rf_model.pkl")
X_train, X_test, y_train, y_test = joblib.load("models/data.pkl")

# Evaluate XGBoost
y_pred_xgb = xgb_model.predict(X_test)
train_acc_xgb = accuracy_score(y_train, xgb_model.predict(X_train))
test_acc_xgb = accuracy_score(y_test, y_pred_xgb)
roc_auc_xgb = roc_auc_score(y_test, y_pred_xgb)

# Evaluate RandomForest
y_pred_rf = rf_model.predict(X_test)
train_acc_rf = accuracy_score(y_train, rf_model.predict(X_train))
test_acc_rf = accuracy_score(y_test, y_pred_rf)
roc_auc_rf = roc_auc_score(y_test, y_pred_rf)

# Print evaluation
print("🔹 **XGBoost Results**")
print(f"Train Accuracy: {train_acc_xgb:.2f}, Test Accuracy: {test_acc_xgb:.2f}, ROC AUC: {roc_auc_xgb:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred_xgb))

print("\n🔹 **RandomForest Results**")
print(f"Train Accuracy: {train_acc_rf:.2f}, Test Accuracy: {test_acc_rf:.2f}, ROC AUC: {roc_auc_rf:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred_rf))
