import csv 
import os

print ("Welcome to Places Explorer")

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