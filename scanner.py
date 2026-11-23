#the scanner finds areas geographically similar to where known archaeological sites already exist

#imports
import joblib
import pandas as pd

#create model object
model = joblib.load("models/archaeology_model.pkl")

results = []

for lat in range(20, 35):
    for lon in range(25, 37):

        sample = pd.DataFrame([[lat, lon]],columns=["Latitude", "Longitude"])

        probability = model.predict_proba(sample)[0][1]

        results.append([lat, lon, probability])

df = pd.DataFrame(results,columns=["Latitude","Longitude","Probability"])

df = df.sort_values("Probability",ascending=False)

print(df.head(20))

df.to_csv("potential_sites.csv",index=False)

#see potential_sites.csv for the identified areas with high and low probability of archaeological potential