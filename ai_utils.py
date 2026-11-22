from geo_utils import calculate_distance


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

from collections import Counter

def predict_civilization(nearby_sites):

    civilizations = []

    for site in nearby_sites:
        civilizations.append(site[1])

    counts = Counter(civilizations)

    return counts.most_common(1)[0][0]