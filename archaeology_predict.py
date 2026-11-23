# the archaeology_predict.py file is used to predict the archaeological potential of a given location based on its latitude and longitude using a pre-trained model.

# imports
import joblib
import pandas as pd

# load trained model
model = joblib.load("models/archaeology_model.pkl")

latitude = float(input("Latitude: "))
longitude = float(input("Longitude: "))

# create a dataframe with the input coordinates
sample = pd.DataFrame([[latitude, longitude]],columns=["Latitude", "Longitude"])

# for the given coordinates, predict the probability of archaeological potential
probability = model.predict_proba(sample)[0][1]

print(f"\nArchaeological Potential: {probability:.2%}")