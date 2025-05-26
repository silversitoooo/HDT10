import unittest
import sys
import os

# Añadir el directorio principal al path para importar correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import Graph
from src.floyd_warshall import floyd_warshall
from src.utils import find_graph_center

class TestFloydWarshall(unittest.TestCase):
    """
    Clase de pruebas para el algoritmo de Floyd-Warshall.
    
    Contiene métodos para probar la correctitud del algoritmo
    en diversos escenarios y casos de prueba.
    """

    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba.
        
        Inicializa un grafo de prueba con varias aristas para ser
        utilizado en las pruebas del algoritmo.
        """
        self.graph = Graph()
        # Añadir aristas con los 4 parámetros necesarios (normal, lluvia, nieve, tormenta)
        self.graph.add_edge("A", "B", 1, 2, 3, 4)
        self.graph.add_edge("B", "C", 2, 3, 4, 5)
        self.graph.add_edge("A", "C", 4, 5, 6, 7)
        self.graph.add_edge("C", "D", 1, 2, 3, 4)
        
        # Añadir aristas faltantes para que C pueda alcanzar todos los nodos
        self.graph.add_edge("C", "A", 2, 3, 4, 5)
        self.graph.add_edge("C", "B", 1, 2, 3, 4)
        self.graph.add_edge("D", "C", 1, 2, 3, 4)
        self.graph.add_edge("B", "A", 3, 4, 5, 6)
        self.graph.add_edge("D", "A", 6, 7, 8, 9)  # Ruta larga de D a A

    def test_shortest_paths(self):
        """
        Prueba el cálculo de caminos más cortos.
        
        Verifica que el algoritmo de Floyd-Warshall calcule correctamente
        las distancias más cortas entre todos los pares de vértices.
        """
        distance_matrix, path_matrix = floyd_warshall(self.graph)
        
        # Obtener índices de los vértices
        a_idx = self.graph.vertices.index("A")
        b_idx = self.graph.vertices.index("B")
        c_idx = self.graph.vertices.index("C")
        d_idx = self.graph.vertices.index("D")
        
        # Verificar distancias usando los índices
        self.assertEqual(distance_matrix[a_idx][b_idx], 1)
        self.assertEqual(distance_matrix[a_idx][c_idx], 3)  # A->B->C es más corto que A->C
        self.assertEqual(distance_matrix[a_idx][d_idx], 4)  # A->B->C->D
        self.assertEqual(distance_matrix[b_idx][c_idx], 2)
        self.assertEqual(distance_matrix[b_idx][d_idx], 3)  # B->C->D
        self.assertEqual(distance_matrix[c_idx][d_idx], 1)

    def test_no_path(self):
        """
        Prueba el comportamiento cuando no existe un camino.
        
        Verifica que el algoritmo maneje correctamente los casos
        donde no existe una ruta entre dos vértices.
        """
        self.graph.add_vertex("E")
        self.graph.add_vertex("F")
        self.graph.add_edge("E", "F", 5, 6, 7, 8)
        distance_matrix, path_matrix = floyd_warshall(self.graph)
        
        # No hay camino de A a E o F
        a_idx = self.graph.vertices.index("A")
        e_idx = self.graph.vertices.index("E")
        self.assertEqual(distance_matrix[a_idx][e_idx], float('inf'))

    def test_center_of_graph(self):
        """
        Prueba el cálculo del centro del grafo.
        
        Verifica que se determine correctamente el centro del grafo
        basado en las distancias calculadas por Floyd-Warshall.
        """
        distance_matrix, _ = floyd_warshall(self.graph)
        center = find_graph_center(distance_matrix, self.graph)
        
        # El centro debería ser C porque minimiza la máxima distancia
        self.assertEqual(center, "C")

if __name__ == '__main__':
    unittest.main()