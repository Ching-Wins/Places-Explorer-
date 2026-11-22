from geo_utils import calculate_distance
from collections import Counter

def find_nearest_sites(latitude, longitude, places):

    nearby_sites = []

    for place in places:

        distance = calculate_distance(
            latitude,
            longitude,
            place["Latitude"],
            place["Longitude"])

        nearby_sites.append(
            (
                place["Name of Location"],
                place["Civilization"],
                distance
            )
        )

    nearby_sites.sort(key=lambda x: x[2])

    return nearby_sites[:5]

def predict_civilization(nearby_sites):

    civilizations = []

    for site in nearby_sites:
        civilizations.append(site[1])

    counts = Counter(civilizations)

    return counts.most_common(1)[0][0]

def prediction_confidence(nearby_sites):

    civilizations = []

    for site in nearby_sites:
        civilizations.append(site[1])

    counts = Counter(civilizations)

    most_common_count = counts.most_common(1)[0][1]

    confidence = (
        most_common_count / len(nearby_sites)
    ) * 100

    return confidence

def find_clusters(places, max_distance=50):

    clusters = []

    for place in places:

        cluster = []

        for other_place in places:

            if place == other_place:
                continue

            distance = calculate_distance(
                place["Latitude"],
                place["Longitude"],
                other_place["Latitude"],
                other_place["Longitude"]
            )

            if distance <= max_distance:
                cluster.append(other_place["Name of Location"])

        clusters.append(
            (place["Name of Location"], cluster)
        )

    return clusters