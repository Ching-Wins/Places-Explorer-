import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load data
df = pd.read_csv("data/archsites_training.csv")
print(df["Site"].isna().sum())
print(df[df["Site"].isna()])

# Features
X = df[["Latitude", "Longitude"]]

# Target
y = df["Site"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2%}")

# Save model
joblib.dump(model, "models/archaeology_model.pkl")

print("Model saved")