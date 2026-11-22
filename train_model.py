import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv(
    "places.csv",
    encoding="utf-8")

print(data.columns)

data["Latitude"] = pd.to_numeric(
    data["Latitude"],
    errors="coerce")

data["Longitude"] = pd.to_numeric(
    data["Longitude"],
    errors="coerce")

data = data.dropna(
    subset=["Latitude", "Longitude"])

X = data[["Latitude", "Longitude"]]

y = data["Civilization"]

model = KNeighborsClassifier(
    n_neighbors=5)

model.fit(X, y)

print("Training Complete!")

# explorer enters valid coordinates
latitude = float(input("Latitude: "))

if latitude < -90 or latitude > 90:
    print("Invalid latitude.")
    exit()

longitude = float(input("Longitude: "))

if longitude < -180 or longitude > 180:
    print("Invalid longitude.")
    exit()

# create a dataframe with same feature names
prediction_data = pd.DataFrame(
    [[latitude, longitude]],
    columns=["Latitude", "Longitude"])

prediction = model.predict(prediction_data)

print(
    f"\nPredicted Civilization: "
    f"{prediction[0]}")

# split data for training
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42)

# train the model
model.fit(X_train,y_train)

# evaluate the model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: "f"{accuracy * 100:.2f}%")

joblib.dump(model,"places_model.pkl")

print("Model Saved")