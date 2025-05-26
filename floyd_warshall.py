def floyd_warshall(graph):
    """
    Implementa el algoritmo de Floyd-Warshall para encontrar los caminos más cortos.
    
    Args:
        graph (Graph): El grafo a analizar
        
    Returns:
        tuple: (matriz_distancias, matriz_caminos) para las rutas más cortas
    """
    n = len(graph.vertices)
    
    # Inicializar matrices
    dist = []
    for i in range(n):
        dist.append(graph.adjacency_matrix[i].copy())
    
    # Matriz para reconstruir caminos
    path = [[-1 if dist[i][j] == float('inf') else i for j in range(n)] for i in range(n)]
    
    # Algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        path[i][j] = path[k][j]
    
    return dist, path

def reconstruct_path(next_node, start, end):
    """
    Reconstruye el camino más corto entre dos vértices.
    
    Utiliza la matriz next_node generada por el algoritmo de Floyd-Warshall
    para reconstruir el camino desde el vértice start hasta el vértice end.
    
    Args:
        next_node (list): Matriz con información para reconstruir caminos
        start (int): Índice del vértice de inicio
        end (int): Índice del vértice de destino
        
    Returns:
        list: Lista ordenada de vértices que forman el camino más corto,
              o lista vacía si no existe un camino
    """
    if next_node[start][end] is None:
        return []
    path = []
    while start != end:
        path.append(start)
        start = next_node[start][end]
    path.append(end)
    return path

def calculate_graph_center(distance):
    """
    Calcula el centro del grafo.
    
    El centro del grafo es el vértice que tiene la menor excentricidad,
    donde la excentricidad es la distancia máxima a cualquier otro vértice.
    
    Args:
        distance (list): Matriz de distancias más cortas entre todos los pares
        
    Returns:
        int: Índice del vértice que es el centro del grafo
    """
    center = None
    min_max_distance = float('inf')

    for i in range(len(distance)):
        max_distance = max(distance[i])
        if max_distance < min_max_distance:
            min_max_distance = max_distance
            center = i

    return center