# heatmap interactive

# imports
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

import folium
from folium.plugins import HeatMap

# added after initial training
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# load the training data
df = pd.read_csv("Data/archsites_training.csv")

# create features
location_type_features = pd.get_dummies(df["Location Type"], prefix="Type")

X = pd.concat([df[["Latitude", "Longitude"]],location_type_features], axis=1)

y = df["Site"]

# train model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# split the data into training and testing sets (after initial training)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test,predictions)

print(f"Accuracy: {accuracy:.3f}")

print(classification_report(y_test,predictions))

# create prediction grid: define boundaries of the data
lat_min = df["Latitude"].min()
lat_max = df["Latitude"].max()

lon_min = df["Longitude"].min()
lon_max = df["Longitude"].max()

# create prediction grid: define grid size
grid_size = 100
lat_points = np.linspace(lat_min,lat_max,grid_size)
lon_points = np.linspace(lon_min,lon_max,grid_size)

# create prediction grid: generate combinations of latitude and longitude points
grid = []
for lat in lat_points:
    for lon in lon_points:
        grid.append([lat, lon])

# create prediction grid: convert to dataframe
grid_df = pd.DataFrame(grid,columns=["Latitude","Longitude"])

# match training columns with grid columns
dummy_grid = pd.DataFrame(0,index=grid_df.index,columns=location_type_features.columns)
grid_df = pd.concat([grid_df, dummy_grid],axis=1)

# add prediction probabilities to the grid dataframe
grid_df["Probability"] = model.predict_proba(grid_df[X.columns])[:, 1]

# create a folium map centered on the mean latitude and longitude of the data
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=5)

# create a heatmap layer using the latitude, longitude, and probability columns
heat_data = []

for _, row in grid_df.iterrows():

    if row["Probability"] > 0.80:

        heat_data.append([
            row["Latitude"],
            row["Longitude"],
            row["Probability"]])

HeatMap(heat_data, radius=20, blur=25, max_zoom=8).add_to(m)

# add site and non-site markers to the map
for _, row in df.iterrows():
    color = "green" if row["Site"] == 1 else "red"

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=3,
        popup=row["Name of Location"],
        color=color,
        fill=True).add_to(m)

# add interactive popup
folium.CircleMarker(
    location=[row["Latitude"], row["Longitude"]],
    radius=3,
    popup=f"{row['Name of Location']} | Site: {row['Site']}",
    color=color,
    fill=True).add_to(m)

# save the map to an HTML file
m.save("archaeology_probability_map.html")

print ("Map saved") 