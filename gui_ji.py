import json
from geopy.distance import geodesic
from datetime import datetime, timedelta
import random


def load_locations_from_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def calculate_distance(start, end):

    return geodesic(start, end).meters


def generate_track_updated(distance, locations):

    current_distance = 0
    start_index = random.randint(0, len(locations) - 1)
    current_location = locations[start_index]
    result = []

    start_time = datetime.now() - timedelta(minutes=30)
    path = [current_location]  # Initialize path with the start location

    while current_distance < distance and current_location["edge"]:
        # Pick the next location from the edge list
        next_index = current_location["edge"][0]  # Simplification: Always pick the first edge
        next_location = next(locations for locations in locations if locations["id"] == next_index)

        # Correctly extract and swap lat and lng for distance calculation
        start_lat, start_lng = [float(coord) for coord in current_location["location"].split(',')]
        end_lat, end_lng = [float(coord) for coord in next_location["location"].split(',')]
        start_coord = (start_lng, start_lat)  # Swapping to match (lat, lng) format expected by geodesic
        end_coord = (end_lng, end_lat)  # Swapping to match (lat, lng) format
        go_distance = calculate_distance(start_coord, end_coord)
        current_distance += go_distance
        if current_distance >= distance:

            break

        path.append(next_location)
        current_location = next_location

    for loc in path:
        lat, lng = [float(c) for c in loc["location"].split(',')]
        accuracy = random.uniform(1, 10)  # Generate a random accuracy value between 1 and 10
        # Assuming an average speed to calculate time to reach each point
        average_speed_m_s = random.uniform(1.4, 4.0)  # Random walking speed between 1.4 m/s to 4 m/s
        time_to_next_point_s = go_distance / average_speed_m_s
        start_time += timedelta(seconds=time_to_next_point_s)
        time_ms = int(start_time.timestamp() * 1000)  # Convert to milliseconds

        result.append(f"{lat}-{lng}-{time_ms}-{round(accuracy, 1)}")

    return result

def run( file_path = 'map_cuit_hkg.json',distance=5000):
    locations = load_locations_from_file(file_path)
    track = generate_track_updated(distance, locations)
    print(f'{file_path}')
    return track
