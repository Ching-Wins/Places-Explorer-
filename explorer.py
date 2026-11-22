import csv 
import os

from geo_utils import calculate_distance

def load_places():
    places = []

    if os.path.isfile("places.csv"):
        with open("places.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                places.append(row)

    return places

def calculate_similarity(place1, place2):
    score = 0

    if place1["Location Type"] == place2["Location Type"]:
        score += 1

    if place1["Civilization"] == place2["Civilization"]:
        score += 1

    return score

print ("Welcome to Places Explorer")
print ("A. Add Discovery")
print ("B. View Discovery")
print ("C. Search Discovery")
print ("D. Recommend Similar Places")
print ("E. Find Nearby Places")

choice = input ("Choose an option: ")

if choice.upper() == "A":
    name = input ("Name of Location: ")
    location_type = input ("Location Type: ")
    latitude = input ("Latitude: ")
    longitude = input ("Longitude: ")
    civilization = input ("Civilization: ")
    notes = input ("Notes: ")

    file_exists = os.path.isfile('places.csv')

    with open('places.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Name of Location', 'Location Type', 'Latitude', 'Longitude', 'Civilization', 'Notes'])
        writer.writerow([name, location_type, latitude, longitude, civilization, notes])

    print ("\nLocation saved successfully")

elif choice.upper() == "B":
    if not os.path.isfile('places.csv'):
        print("\nNo discoveries recorded.")

    else:
        print("\n=== Discovery ===")
        with open('places.csv', mode='r') as file:
            reader = csv.DictReader(file) 
            for row in reader:
                print("\n=== Discovery #{} ===".format(reader.line_num - 1))
                print(row["Name of Location"])
                print(row["Location Type"])
                print(row["Latitude"])
                print(row["Longitude"])
                print(row["Civilization"])
                print(row["Notes"])

elif choice.upper() == "C":
    if not os.path.isfile('places.csv'):
        print("\nNo discoveries recorded.")

    else:
        search_term = input ("\nSearch by term: ").strip().lower()
        found = False 

        with open('places.csv', mode='r') as file:
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

elif choice.upper() == "D":

    if not os.path.isfile('places.csv'):
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

            print("\n=== Recommended Similar Places ===")

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

elif choice.upper() == "E":

    if not os.path.isfile('places.csv'):
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
            print("\n=== Nearby Places ===")

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