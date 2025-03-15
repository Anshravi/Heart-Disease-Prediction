import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/heart.csv")

# Define features and target
X = df.drop(columns=["target"])
y = df["target"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save processed data
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump((X_train_scaled, X_test_scaled, y_train, y_test), "models/data.pkl")

print("✅ Data preprocessing completed and saved!")

