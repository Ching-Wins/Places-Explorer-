import pandas as pd
import joblib

model = joblib.load("places_model.pkl")

print("Places Explorer ML Predictor")

latitude = float(input("Latitude: "))

if latitude < -90 or latitude > 90:
    print("Invalid latitude.")
    exit()

longitude = float(input("Longitude: "))

if longitude < -180 or longitude > 180:
    print("Invalid longitude.")
    exit()

prediction_data = pd.DataFrame(
    [[latitude, longitude]],
    columns=["Latitude", "Longitude"])

prediction = model.predict(prediction_data)

# add prediction confidence
prediction = model.predict(prediction_data)

probabilities = model.predict_proba(prediction_data)

classes = model.classes_

print(f"\nPredicted Civilization: "f"{prediction[0]}")

print("\nConfidence Scores:")

for civilization, probability in zip(classes,probabilities[0]):
    if probability > 0:
        print(f"{civilization}: "f"{probability * 100:.2f}%")