from src.graph import Graph  # Cambiado de 'from graph import Graph'

def read_graph_from_file(filename):
    """
    Lee un grafo desde un archivo de texto con formato específico.
    
    El archivo debe tener el formato:
    Ciudad1 Ciudad2 tiempoNormal tiempoLluvia tiempoNieve tiempoTormenta
    
    Args:
        filename (str): Ruta del archivo a leer
        
    Returns:
        Graph: Objeto grafo con los datos cargados
        
    Raises:
        FileNotFoundError: Si no se encuentra el archivo
    """
    graph = Graph()
    line_number = 0
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line_number += 1
                line = line.strip()
                
                # Ignorar línea de encabezado o vacía
                if not line or line.startswith('//') or line.startswith('#'):
                    continue
                    
                # Ignorar líneas que parezcan encabezados (contienen "Ciudad")
                if "Ciudad" in line and "tiempo" in line:
                    continue
                
                parts = line.split()
                if len(parts) != 6:
                    print(f"Formato incorrecto en línea {line_number}: {line}")
                    continue
                    
                try:
                    city1 = parts[0]
                    city2 = parts[1]
                    normal_time = float(parts[2])
                    rain_time = float(parts[3])
                    snow_time = float(parts[4])
                    storm_time = float(parts[5])
                    
                    # Agregar la arista al grafo
                    graph.add_edge(city1, city2, normal_time, rain_time, snow_time, storm_time)
                    
                except ValueError:
                    print(f"Error al convertir tiempos a números en línea: {line}")
        
        print(f"Grafo cargado con {graph.get_vertex_count()} ciudades")
        return graph
        
    except FileNotFoundError:
        print(f"No se encontró el archivo: {filename}")
        # Crear un grafo vacío para evitar errores
        return graph

def format_output(shortest_path, distance):
    """
    Formatea la salida para mostrar el camino más corto.
    
    Args:
        shortest_path (list): Lista de ciudades que forman el camino más corto
        distance (float): Distancia total del camino
        
    Returns:
        str: Cadena formateada para mostrar al usuario
    """
    if shortest_path:
        path_str = " -> ".join(shortest_path)
        return f"Shortest path: {path_str} with a total time of {distance} hours."
    else:
        return "No path found."

def display_adjacency_matrix(matrix):
    """
    Muestra una matriz de adyacencia en la consola.
    
    Args:
        matrix (list): Matriz de adyacencia a mostrar
    """
    for row in matrix:
        print(" | ".join(map(str, row)))

def display_shortest_path(start_city, end_city, distance_matrix, path_info, graph):
    """
    Muestra la ruta más corta entre dos ciudades.
    
    Args:
        start_city (str): Ciudad de origen
        end_city (str): Ciudad de destino
        distance_matrix (list): Matriz de distancias más cortas
        path_info (list): Matriz de caminos para reconstrucción
        graph (Graph): El grafo que contiene las ciudades
    """
    # Convertir los nombres de ciudades a minúsculas para comparación
    start_city = start_city.lower()
    end_city = end_city.lower()
    
    # Obtener los índices de las ciudades
    start_idx = -1
    end_idx = -1
    
    for idx, city in enumerate(graph.vertices):
        if city.lower() == start_city:
            start_idx = idx
        if city.lower() == end_city:
            end_idx = idx
    
    if start_idx == -1:
        print(f"Error: La ciudad '{start_city}' no existe en el grafo.")
        return
        
    if end_idx == -1:
        print(f"Error: La ciudad '{end_city}' no existe en el grafo.")
        return
    
    # Obtener la distancia
    distance = distance_matrix[start_idx][end_idx]
    
    if distance == float('inf'):
        print(f"No existe ruta de {graph.vertices[start_idx]} a {graph.vertices[end_idx]}")
        return
    
    # Reconstruir la ruta
    path = []
    current = end_idx
    
    while current != start_idx:
        path.append(graph.vertices[current])
        current = path_info[start_idx][current]
        if current == -1:  # No hay camino
            break
    
    path.append(graph.vertices[start_idx])
    path.reverse()
    
    # Mostrar la ruta
    print(f"\nRuta más corta de {graph.vertices[start_idx]} a {graph.vertices[end_idx]}:")
    print(f"Distancia: {distance} horas")
    print("Camino: " + " -> ".join(path))

def find_graph_center(distance_matrix, graph):
    """
    Encuentra el centro del grafo.
    
    El centro del grafo es el vértice cuya máxima distancia a cualquier
    otro vértice es mínima.
    
    Args:
        distance_matrix (list): Matriz de distancias más cortas
        graph (Graph): El grafo que contiene los vértices
        
    Returns:
        str: Nombre de la ciudad que es el centro del grafo
    """
    n = len(graph.vertices)
    min_eccentricity = float('inf')
    center_idx = -1
    eccentricities = {}  # Para guardar la excentricidad de cada ciudad
    
    # Calcular la excentricidad de cada vértice
    for i in range(n):
        eccentricity = 0  # Inicializar con el valor más pequeño posible
        has_unreachable = False  # Bandera para vértices inalcanzables
        
        for j in range(n):
            if i != j:  # No consideramos la distancia a sí mismo
                if distance_matrix[i][j] == float('inf'):
                    # Si hay un vértice inalcanzable, la excentricidad es infinita
                    has_unreachable = True
                    break
                eccentricity = max(eccentricity, distance_matrix[i][j])
        
        # Si hay vértices inalcanzables, la excentricidad es infinita
        if has_unreachable:
            eccentricities[graph.vertices[i]] = float('inf')
        else:
            eccentricities[graph.vertices[i]] = eccentricity
            # Actualizar el centro si encontramos una excentricidad menor
            if eccentricity < min_eccentricity:
                min_eccentricity = eccentricity
                center_idx = i
    
    # Mostrar información para depuración
    print("\nExcentricidades de las ciudades:")
    sorted_cities = sorted(eccentricities.items(), key=lambda x: float('inf') if x[1] == float('inf') else x[1])
    for city, ecc in sorted_cities:
        if ecc == float('inf'):
            print(f"  {city}: ∞ (no puede alcanzar todas las ciudades)")
        else:
            print(f"  {city}: {ecc:.2f}{' <- CENTRO' if city == graph.vertices[center_idx] else ''}")
    
    if center_idx != -1:
        return graph.vertices[center_idx]
    else:
        return "No se pudo determinar el centro del grafo"
