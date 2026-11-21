import csv 
import os

print ("Welcome to Places Explorer")
print ("A. Add Discovery")
print ("B. View Discovery")
print ("C. Search Discovery")

choice = input ("Choose an option: ")

if choice.upper() == "A":
    name = input ("Name of Location: ")
    latitude = input ("Latitude: ")
    longitude = input ("Longitude: ")
    notes = input ("Notes: ")

    file_exists = os.path.isfile('places.csv')

    with open('places.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Name', 'Latitude', 'Longitude', 'Notes'])
        writer.writerow([name, latitude, longitude, notes])

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
                print(f"Latitude: {row[1]}")
                print(f"Longitude: {row[2]}")
                print(f"Notes: {row[3]}")

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
                    print(f"Latitude: {row[1]}")
                    print(f"Longitude: {row[2]}")
                    print(f"Notes: {row[3]}")

        if not found:
            print("\nTerm does not exist.")