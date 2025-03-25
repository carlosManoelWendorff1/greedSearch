import codecs
import json

def load_map():
    with codecs.open('cidades.json', 'r', encoding='utf-8') as file:
        return json.load(file)  # Convert JSON into a dictionary

def greedy_path(map_data, origin, destination):
    if origin not in map_data or destination not in map_data:
        return None, 0

    path = [origin]
    total_distance = 0
    current = origin

    while current != destination:
        neighbors = map_data.get(current, {})
        if not neighbors:
            return None, 0

        next_city = min(neighbors, key=neighbors.get)
        total_distance += neighbors[next_city]
        path.append(next_city)

        if next_city == destination:
            break

        current = next_city

    return path, total_distance

def main():
    map_data = load_map()

    print("\nAvailable cities:")
    for city in sorted(map_data.keys()):
        print(city)

    origin = raw_input("\nEnter the origin city: ").strip().title()
    destination = raw_input("Enter the destination city: ").strip().title()

    if origin not in map_data:
        print("Error: The city was not found on the map.")
        return
    if destination not in map_data:
        print("Error: The city was not found on the map.")
        return

    path, distance = greedy_path(map_data, origin, destination)

    if path:
        print("\nPath found:", " -> ".join(path))
        print("Total distance:", distance, "km")
    else:
        print("\nCould not find a path.")

if __name__ == "__main__":
    main()
