import csv 
import os

print ("Welcome to Places Explorer")
print ("A. Add Discovery")
print ("B. View Discovery")
print ("C. Search Discovery")

choice = input ("Choose an option: ")

if choice.upper() == "A":
    name = input ("Name of Location: ")
    location_type = input ("Location Type: ")
    latitude = input ("Latitude: ")
    longitude = input ("Longitude: ")
    civilization = input ("Civilization: ")
    time_period = input ("Time Period: ")
    water_source = input ("Water Source: ")
    status = input ("Status: ")
    notes = input ("Notes: ")

    file_exists = os.path.isfile('places.csv')

    with open('places.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Name of Location', 'Location Type', 'Latitude', 'Longitude', 'Civilization', 'Time Period', 'Water Source', 'Status', 'Notes'])
        writer.writerow([name, location_type, latitude, longitude, civilization, time_period, water_source, status, notes])

    print ("\nLocation saved successfully")

elif choice.upper() == "B":
    if not os.path.isfile('places.csv'):
        print("\nNo discoveries recorded.")

    else:
        print("\n=== Discovery ===")
        with open('places.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None) 
            for number, row in enumerate(reader, start=1):
                print(f"\nDiscovery # {number}") 
                print(f"Name: {row[0]}")
                print(f"Location Type: {row[1]}")
                print(f"Latitude: {row[2]}")
                print(f"Longitude: {row[3]}")
                print(f"Civilization: {row[4]}")
                print(f"Time Period: {row[5]}")
                print(f"Water Source: {row[6]}")
                print(f"Status: {row[7]}")
                print(f"Notes: {row[8]}")

elif choice.upper() == "C":
    if not os.path.isfile('places.csv'):
        print("\nNo discoveries recorded.")

    else:
        search_term = input ("\nSearch by term: ").strip().lower()
        found = False 

        with open('places.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if any(search_term in str(field).lower() for field in row):
                    found = True
                    print("\nMatch found")
                    print(f"\nName: {row[0]}")
                    print(f"Location Type: {row[1]}")
                    print(f"Latitude: {row[2]}")
                    print(f"Longitude: {row[3]}")
                    print(f"Civilization: {row[4]}")
                    print(f"Time Period: {row[5]}")
                    print(f"Water Source: {row[6]}")
                    print(f"Status: {row[7]}")
                    print(f"Notes: {row[8]}")

        if not found:
            print("\nTerm does not exist.")