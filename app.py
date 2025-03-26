import codecs
import json
import matplotlib.pyplot as plt
import networkx as nx
import time
import random

def load_map():
    with codecs.open('cidades.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_positions(map_data):
    """Gera posições aleatórias para as cidades no gráfico."""
    return {city: (random.uniform(0, 100), random.uniform(0, 100)) for city in map_data.keys()}

def greedy_path(map_data, origin, destination, graph, pos):
    if origin not in map_data or destination not in map_data:
        return None, 0

    path = [origin]
    total_distance = 0
    current = origin
    visited = set()

    print("\nExploring path:")

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 7))

    while current != destination:
        print(f"Currently in: {current}")
        visited.add(current)

        draw_map(graph, pos, path, current, ax)
        time.sleep(1)

        neighbors = map_data.get(current, {})
        if not neighbors:
            print("No more neighbors. Stuck!")
            return None, 0

        possible_moves = {city: dist for city, dist in neighbors.items() if city not in visited}

        if not possible_moves:
            print(f"Dead end at {current}. Backtracking...")
            path.pop()
            if not path:
                print("No valid path found!")
                return None, 0
            current = path[-1]
            continue

        next_city = min(possible_moves, key=lambda city: (possible_moves[city], heuristic(city, destination, pos)))
        total_distance += neighbors[next_city]
        path.append(next_city)

        if next_city == destination:
            print(f"Arrived at: {destination}")
            break

        current = next_city

    # Remove cidades não visitadas
    clean_map(graph, path, pos)

    draw_map(graph, pos, path, current, ax, final=True)
    plt.ioff()
    plt.show()

    # Exibe o caminho no terminal
    print("\nFinal Path:", " -> ".join(path))
    print("Total distance:", total_distance, "km")

    return path, total_distance

def heuristic(city, destination, pos):
    """Calcula uma heurística baseada na distância Euclidiana."""
    x1, y1 = pos[city]
    x2, y2 = pos[destination]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def draw_map(graph, pos, path, current, ax, final=False):
    """Desenha o mapa e destaca o caminho percorrido."""
    ax.clear()
    ax.set_title("Mapa de Cidades - Busca Gulosa")

    # Mantém apenas as cidades visitadas
    subgraph = graph.subgraph(path)

    nx.draw(subgraph, pos, with_labels=True, node_size=300, node_color="lightgray", edge_color="gray", ax=ax)
    
    edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(subgraph, pos, edgelist=edges_in_path, edge_color="blue", width=2, ax=ax)
    
    nx.draw_networkx_nodes(subgraph, pos, nodelist=[current], node_color="red", node_size=500, ax=ax)
    
    if final:
        nx.draw_networkx_nodes(subgraph, pos, nodelist=path, node_color="green", node_size=400, ax=ax)

    plt.pause(0.5)

def clean_map(graph, path, pos):
    """Remove do grafo e do mapa todas as cidades não percorridas."""
    nodes_to_remove = [city for city in list(graph.nodes) if city not in path]
    
    for city in nodes_to_remove:
        graph.remove_node(city)
        del pos[city]  # Remove a posição para que não seja mais desenhada

def build_graph(map_data):
    """Cria um grafo para visualização e garante posições para todas as cidades."""
    G = nx.Graph()
    
    for city, neighbors in map_data.items():
        G.add_node(city)
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)

    pos = {city: (random.uniform(0, 100), random.uniform(0, 100)) for city in G.nodes}

    return G, pos

def main():
    map_data = load_map()

    print("\nAvailable cities:")
    for city in sorted(map_data.keys()):
        print(city)

    origin = input("\nEnter the origin city: ").strip().title()
    destination = input("Enter the destination city: ").strip().title()

    if origin not in map_data:
        print("Error: The city was not found on the map.")
        return
    if destination not in map_data:
        print("Error: The city was not found on the map.")
        return

    graph, pos = build_graph(map_data)

    path, distance = greedy_path(map_data, origin, destination, graph, pos)

    if not path:
        print("\nCould not find a path.")

if __name__ == "__main__":
    main()
