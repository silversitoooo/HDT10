import unittest
import sys
import os

# Añadir el directorio principal al path para importar correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import Graph
from src.utils import read_graph_from_file

class TestGraph(unittest.TestCase):
    """
    Clase de pruebas para la implementación de Graph.
    
    Contiene métodos para probar la creación, modificación y
    visualización de grafos dirigidos.
    """

    def setUp(self):
        """
        Método que se ejecuta antes de cada prueba.
        
        Inicializa un objeto Graph para ser utilizado en las pruebas.
        """
        self.graph = Graph()

    def test_add_vertex(self):
        """
        Prueba la adición de vértices al grafo.
        
        Verifica que los vértices se agreguen correctamente al grafo.
        """
        self.graph.add_vertex("A")
        self.assertIn("A", self.graph.vertices)
        
    def test_add_edge(self):
        """
        Prueba la adición de aristas al grafo.
        
        Verifica que las aristas se agreguen correctamente y que
        los valores de peso se asignen adecuadamente.
        """
        self.graph.add_edge("A", "B", 5, 6, 7, 8)
        
        # Verificar que los vértices se han añadido
        self.assertIn("A", self.graph.vertices)
        self.assertIn("B", self.graph.vertices)
        
        # Verificar que la arista se ha añadido correctamente
        a_idx = self.graph.vertices.index("A")
        b_idx = self.graph.vertices.index("B")
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 5)  # clima normal por defecto
        
        # Verificar los tiempos para diferentes climas
        edge_key = ("A", "B")
        self.assertEqual(self.graph.weather_times[edge_key]["normal"], 5)
        self.assertEqual(self.graph.weather_times[edge_key]["lluvia"], 6)
        self.assertEqual(self.graph.weather_times[edge_key]["nieve"], 7)
        self.assertEqual(self.graph.weather_times[edge_key]["tormenta"], 8)

    def test_remove_edge(self):
        """
        Prueba la eliminación de aristas del grafo.
        
        Verifica que las aristas se eliminen correctamente del grafo.
        """
        self.graph.add_edge("A", "B", 5, 6, 7, 8)
        
        a_idx = self.graph.vertices.index("A")
        b_idx = self.graph.vertices.index("B")
        
        # Verificar que existe la arista
        self.assertNotEqual(self.graph.adjacency_matrix[a_idx][b_idx], float('inf'))
        
        # Eliminar la arista
        self.graph.remove_edge("A", "B")
        
        # Verificar que ya no existe la arista
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], float('inf'))

    def test_file_operations(self):
        """
        Prueba la lectura de un grafo desde un archivo.
        
        Verifica que la función lee correctamente el grafo desde el archivo
        especificado y lo carga en la estructura de datos.
        """
        # Crear un archivo temporal para pruebas
        test_file = os.path.join(os.path.dirname(__file__), "test_logistica.txt")
        with open(test_file, "w") as f:
            f.write("CiudadA CiudadB 10 15 20 25\n")
            f.write("CiudadB CiudadC 5 6 7 8\n")
        
        try:
            # Leer el grafo desde el archivo
            graph = read_graph_from_file(test_file)
            
            # Verificar que se han cargado las ciudades
            self.assertEqual(graph.get_vertex_count(), 3)
            self.assertIn("CiudadA", graph.vertices)
            self.assertIn("CiudadB", graph.vertices)
            self.assertIn("CiudadC", graph.vertices)
            
            # Verificar las conexiones
            a_idx = graph.vertices.index("CiudadA")
            b_idx = graph.vertices.index("CiudadB")
            c_idx = graph.vertices.index("CiudadC")
            
            self.assertEqual(graph.adjacency_matrix[a_idx][b_idx], 10)
            self.assertEqual(graph.adjacency_matrix[b_idx][c_idx], 5)
        finally:
            # Limpiar el archivo temporal
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_set_weather_condition(self):
        """
        Prueba el cambio de condición climática.
        
        Verifica que al cambiar la condición climática, los pesos
        de las aristas se actualicen correctamente.
        """
        self.graph.add_edge("A", "B", 5, 10, 15, 20)
        
        a_idx = self.graph.vertices.index("A")
        b_idx = self.graph.vertices.index("B")
        
        # Verificar el tiempo con clima normal (por defecto)
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 5)
        
        # Cambiar a clima de lluvia
        self.graph.set_weather_condition("lluvia")
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 10)
        
        # Cambiar a clima de nieve
        self.graph.set_weather_condition("nieve")
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 15)
        
        # Cambiar a clima de tormenta
        self.graph.set_weather_condition("tormenta")
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 20)
        
        # Volver a clima normal
        self.graph.set_weather_condition("normal")
        self.assertEqual(self.graph.adjacency_matrix[a_idx][b_idx], 5)

if __name__ == '__main__':
    unittest.main()