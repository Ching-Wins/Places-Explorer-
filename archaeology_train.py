# this script trains a machine learning model to predict the archaeological potential of a given location based on its latitude and longitude.

# imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# load data
df = pd.read_csv("data/archsites_training.csv")
print(df["Site"].isna().sum())
print(df[df["Site"].isna()])

# features
X = df[["Latitude", "Longitude"]]

# target
y = df["Site"]

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42)

# train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42)

model.fit(X_train, y_train)

# predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2%}")

# save model
joblib.dump(model, "models/archaeology_model.pkl")

print("Model saved")