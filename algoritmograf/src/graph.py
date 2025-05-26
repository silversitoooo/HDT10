class Graph:
    """
    Clase que implementa un grafo dirigido usando matriz de adyacencia.
    
    Attributes:
        vertices (list): Lista de nombres de ciudades (vértices)
        adjacency_matrix (list): Matriz de adyacencia con tiempos de viaje
        weather_times (dict): Diccionario con tiempos para diferentes condiciones
        current_weather (str): Condición climática actual
    """
    
    def __init__(self):
        """
        Inicializa un grafo vacío.
        """
        self.vertices = []
        self.adjacency_matrix = []
        self.weather_times = {}  # Para almacenar tiempos en diferentes condiciones
        self.current_weather = 'normal'  # Condición climática por defecto
    
    def add_vertex(self, vertex):
        """
        Agrega un nuevo vértice (ciudad) al grafo.
        
        Args:
            vertex (str): Nombre de la ciudad
            
        Returns:
            bool: True si se agregó, False si ya existía
        """
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            
            # Expandir la matriz de adyacencia
            if len(self.adjacency_matrix) == 0:
                self.adjacency_matrix = [[float('inf')]]
            else:
                # Agregar una columna de infinitos a cada fila existente
                for row in self.adjacency_matrix:
                    row.append(float('inf'))
                
                # Agregar una nueva fila de infinitos
                new_row = [float('inf')] * len(self.vertices)
                self.adjacency_matrix.append(new_row)
            
            # Distancia a sí mismo es 0
            self.adjacency_matrix[len(self.vertices) - 1][len(self.vertices) - 1] = 0
            
            return True
        return False
    
    def add_edge(self, from_vertex, to_vertex, normal_time, rain_time, snow_time, storm_time):
        """
        Agrega una arista entre dos vértices con tiempos para diferentes condiciones.
        
        Args:
            from_vertex (str): Ciudad origen
            to_vertex (str): Ciudad destino
            normal_time (float): Tiempo con clima normal
            rain_time (float): Tiempo con lluvia
            snow_time (float): Tiempo con nieve
            storm_time (float): Tiempo con tormenta
            
        Returns:
            bool: True si se agregó correctamente
        """
        # Agregar vértices si no existen
        if from_vertex not in self.vertices:
            self.add_vertex(from_vertex)
        if to_vertex not in self.vertices:
            self.add_vertex(to_vertex)
        
        from_idx = self.vertices.index(from_vertex)
        to_idx = self.vertices.index(to_vertex)
        
        # Almacenar todos los tiempos
        edge_key = (from_vertex, to_vertex)
        self.weather_times[edge_key] = {
            'normal': normal_time,
            'lluvia': rain_time,
            'nieve': snow_time,
            'tormenta': storm_time
        }
        
        # Establecer el tiempo actual según el clima actual
        self.adjacency_matrix[from_idx][to_idx] = self.weather_times[edge_key][self.current_weather]
        
        return True
    
    def remove_edge(self, from_vertex, to_vertex):
        """
        Elimina una arista entre dos vértices.
        
        Args:
            from_vertex (str): Ciudad origen
            to_vertex (str): Ciudad destino
            
        Returns:
            bool: True si se eliminó la arista
        """
        # Convertir a minúsculas para hacer la comparación insensible a mayúsculas/minúsculas
        from_vertex_lower = from_vertex.lower()
        to_vertex_lower = to_vertex.lower()
        
        # Buscar los vértices en el grafo
        from_idx = -1
        to_idx = -1
        for idx, city in enumerate(self.vertices):
            if city.lower() == from_vertex_lower:
                from_idx = idx
            if city.lower() == to_vertex_lower:
                to_idx = idx
        
        # Verificar si los vértices existen
        if from_idx == -1 or to_idx == -1:
            print(f"Error: Una o ambas ciudades no existen en el grafo.")
            print(f"Ciudades disponibles: {', '.join(self.vertices)}")
            return False
        
        # Verificar si existe una arista entre estos vértices
        if self.adjacency_matrix[from_idx][to_idx] == float('inf'):
            print(f"Error: No existe tráfico directo entre {self.vertices[from_idx]} y {self.vertices[to_idx]}.")
            return False
        
        # Eliminar la arista
        self.adjacency_matrix[from_idx][to_idx] = float('inf')
        
        # Obtener los nombres originales de las ciudades
        orig_from = self.vertices[from_idx]
        orig_to = self.vertices[to_idx]
        
        # Eliminar del diccionario de tiempos
        edge_key = (orig_from, orig_to)
        if edge_key in self.weather_times:
            del self.weather_times[edge_key]
            
        return True
    
    def set_weather_condition(self, condition):
        """
        Cambia la condición climática y actualiza los tiempos en la matriz.
        
        Args:
            condition (str): Condición climática ('normal', 'lluvia', 'nieve', 'tormenta')
            
        Returns:
            bool: True si se cambió correctamente
        """
        if condition not in ['normal', 'lluvia', 'nieve', 'tormenta']:
            return False
            
        self.current_weather = condition
        
        # Actualizar todas las aristas con los nuevos tiempos
        for edge_key, times in self.weather_times.items():
            from_vertex, to_vertex = edge_key
            from_idx = self.vertices.index(from_vertex)
            to_idx = self.vertices.index(to_vertex)
            
            self.adjacency_matrix[from_idx][to_idx] = times[condition]
            
        return True
    
    def get_vertex_count(self):
        """
        Retorna el número de vértices en el grafo.
        
        Returns:
            int: Número de vértices
        """
        return len(self.vertices)
    
    def display_adjacency_matrix(self):
        """
        Muestra la matriz de adyacencia en un formato legible.
        """
        if not self.vertices:
            print("El grafo está vacío")
            return
            
        print("\nMatriz de Adyacencia (condición actual: " + self.current_weather + "):")
        print("     ", end="")
        
        # Mostrar encabezado con nombres de ciudades
        for city in self.vertices:
            print(f"{city[:8]:<10}", end="")
        print()
        
        # Mostrar filas de la matriz
        for i, city in enumerate(self.vertices):
            print(f"{city[:8]:<8}", end="")
            for j in range(len(self.vertices)):
                if self.adjacency_matrix[i][j] == float('inf'):
                    print("∞      ", end="")
                else:
                    print(f"{self.adjacency_matrix[i][j]:<8.1f}", end="")
            print()