# this script is the main entry point for the Places Explorer application. It provides a command-line interface for users to add, view, search, and analyze archaeological discoveries.

# file imports
import csv
import os
import importlib
import math

# Load optional project modules dynamically so the menu works even if a module is
# not currently resolvable by the editor or is run outside the project directory.
try:
    calculate_distance = importlib.import_module("Initial Testing/geo_utils").calculate_distance
except (ImportError, AttributeError):
    def calculate_distance(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(float, (lat1, lon1, lat2, lon2))
        lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

try:
    _ai_utils = importlib.import_module("Initial Testing/ai_utils")
    find_nearest_sites = _ai_utils.find_nearest_sites
    predict_civilization = _ai_utils.predict_civilization
    prediction_confidence = _ai_utils.prediction_confidence
    find_clusters = _ai_utils.find_clusters
except (ImportError, AttributeError):
    def find_nearest_sites(latitude, longitude, places, limit=5):
        nearby = []
        for place in places:
            distance = calculate_distance(latitude, longitude,
                                          place["Latitude"], place["Longitude"])
            nearby.append((place["Name of Location"], place["Civilization"], distance))
        nearby.sort(key=lambda site: site[2])
        return nearby[:limit]

    def predict_civilization(nearby_sites):
        if not nearby_sites:
            return "Unknown"
        civilizations = {}
        for _, civilization, distance in nearby_sites:
            weight = 1 / (distance + 1)
            civilizations[civilization] = civilizations.get(civilization, 0) + weight
        return max(civilizations, key=civilizations.get)

    def prediction_confidence(nearby_sites):
        if not nearby_sites:
            return 0.0
        civilization = predict_civilization(nearby_sites)
        matching = sum(1 for _, site_civilization, _ in nearby_sites
                       if site_civilization == civilization)
        return (matching / len(nearby_sites)) * 100

    def find_clusters(places, radius_km=50):
        clusters = []
        remaining = list(places)
        while remaining:
            location = remaining.pop(0)
            nearby = []
            kept = []
            for place in remaining:
                distance = calculate_distance(location["Latitude"], location["Longitude"],
                                              place["Latitude"], place["Longitude"])
                if distance <= radius_km:
                    nearby.append(place["Name of Location"])
                else:
                    kept.append(place)
            remaining = kept
            clusters.append((location["Name of Location"], nearby))
        return clusters

# functions to load places from files
def load_places():
    places = []

    if os.path.isfile("Data/places.csv"):
        with open("Data/places.csv", mode="r", encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                places.append(row)

    return places

# function to calculate similarity score between two places
def calculate_similarity(place1, place2):
    score = 0

    if place1["Location Type"] == place2["Location Type"]:
        score += 1

    if place1["Civilization"] == place2["Civilization"]:
        score += 1

    return score

# main program displays menu and handles user input
print ("Welcome to Places Explorer")
print ("A. Add Discovery")
print ("B. View Discovery")
print ("C. Search Discovery")
print ("D. Recommend Similar Places")
print ("E. Find Nearby Places")
print ("F. Civilization Predictor")
print ("G. ID Site Clusters")

choice = input ("Choose an option: ")

# function choice A
if choice.upper() == "A":
    name = input ("Name of Location: ")
    location_type = input ("Location Type: ")
    latitude = input ("Latitude: ")
    longitude = input ("Longitude: ")
    civilization = input ("Civilization: ")
    notes = input ("Notes: ")

    file_exists = os.path.isfile('Data/places.csv')

    with open('Data/places.csv', mode='a', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Name of Location', 'Location Type', 'Latitude', 'Longitude', 'Civilization', 'Notes'])
        writer.writerow([name, location_type, latitude, longitude, civilization, notes])

    print ("\nLocation saved successfully")

# function choice B
elif choice.upper() == "B":
    if not os.path.isfile('Data/places.csv'):
        print("\nNo discoveries recorded.")

    else:
        print("\n>>> Discovery <<<")
        with open('Data/places.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file) 
            for row in reader:
                print("\n=== Discovery #{} ===".format(reader.line_num - 1))
                print(row["Name of Location"])
                print(row["Location Type"])
                print(row["Latitude"])
                print(row["Longitude"])
                print(row["Civilization"])
                print(row["Notes"])

# function choice C
elif choice.upper() == "C":
    if not os.path.isfile('Data/places.csv'):
        print("\nNo discoveries recorded.")

    else:
        search_term = input ("\nSearch by term: ").strip().lower()
        found = False 

        with open('Data/places.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if search_term in row["Name of Location"].strip().lower() or search_term in row["Location Type"].strip().lower():
                    found = True
                    print("\n=== Match Found ===")
                    print(row["Name of Location"])
                    print(row["Location Type"])
                    print(row["Latitude"])
                    print(row["Longitude"])
                    print(row["Civilization"])
                    print(row["Notes"])
        if not found:
            print("\nTerm does not exist.")

# function choice D
elif choice.upper() == "D":

    if not os.path.isfile('Data/places.csv'):
        print("\nNo discoveries recorded.")

    else:
        places = load_places()
        recommendations = []

        for i in range(len(places)):
            for j in range(i + 1, len(places)):

                similarity_score = calculate_similarity(
                    places[i],
                    places[j])

                if similarity_score > 0:
                    recommendations.append(
                        (places[i], places[j], similarity_score))

        if recommendations:

            print("\n>>> Recommended Similar Places <<<")

            recommendations.sort(
                key=lambda x: x[2],
                reverse=True)

            for place1, place2, score in recommendations:

                print(
                    f"\n{place1['Name of Location']} and "
                    f"{place2['Name of Location']} "
                    f"have a similarity score of {score}.")

        else:
            print("\nNo similar places found.")

# function choice E
elif choice.upper() == "E":

    if not os.path.isfile('Data/places.csv'):
        print("\nNo discoveries recorded.")

    else:
        places = load_places()
        place_name = input("\nSelect a place by name: ").strip().lower()
        selected_place = next(
            (place for place in places
             if place["Name of Location"].strip().lower() == place_name),
            None)

        if selected_place is None:
            print("\nPlace does not exist.")
        else:
            print("\n>>> Nearby Places <<<")

            nearby_places = []

            for place in places:

                if place == selected_place:
                    continue

                distance = calculate_distance(
                    selected_place["Latitude"],
                    selected_place["Longitude"],
                    place["Latitude"],
                    place["Longitude"])

                nearby_places.append((place["Name of Location"], distance))

            nearby_places.sort(key=lambda x: x[1])

            for name, distance in nearby_places:
                print(f"{name} ({distance:.2f} km)")

# function choice F
elif choice.upper() == "F":

    latitude = input("Latitude: ")
    longitude = input("Longitude: ")

    places = load_places()

    nearby_sites = find_nearest_sites(
        latitude,
        longitude,
        places)

    print("\nNearest Sites:")

    for site in nearby_sites:
        print(
            f"{site[0]} "
            f"({site[1]}) "
            f"- {site[2]:.2f} km")

    prediction = predict_civilization(nearby_sites)
    print(f"\nPredicted Civilization: {prediction}")

    confidence = prediction_confidence(nearby_sites)
    print(confidence)
    print(type(confidence))
    print(f"Confidence: {confidence:.2f}%")

# function choice G
elif choice.upper() == "G":

    if not os.path.isfile('Data/places.csv'):
        print("\nNo discoveries recorded.")

    else:

        places = load_places()

        clusters = find_clusters(places)

        print("\n >>> Site Clusters <<<")

        for location, nearby_sites in clusters:

            if nearby_sites:

                print(f"\n{location}")

                for site in nearby_sites:
                    print(f"  - {site}")